from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from typing import List, Dict, Optional
import logging

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)

class PriceService:
    BASE_QUERY = """
        SELECT day, AVG(price) as average_price, COUNT(price)
        FROM prices
        {join_clause}
        WHERE {where_clause}
            AND day BETWEEN :date_from AND :date_to
        GROUP BY day
        ORDER BY day
    """

    @staticmethod
    def calculate_average_prices(date_from: str, date_to: str, origin: str, destination: str) -> List[
        Dict[str, Optional[float]]]:
        """
        Calculate average prices based on the given origin and destination.

        Returns:
            List[Dict[str, Optional[float]]]: List of dictionaries containing the day and average price.
        """
        try:
            # Fetch slugs for the origin and destination regions
            region_service = RegionService()
            origin_region_slugs = region_service.fetch_child_slugs(origin)
            destination_region_slugs = region_service.fetch_child_slugs(destination)

            # Build the SQL query based on the available slugs
            query, params = PriceService._build_query(origin_region_slugs, destination_region_slugs, origin, destination, date_from, date_to)
            result = db.session.execute(query, params)

            # Process and return the price data
            return PriceService._process_price_data(result)
        except Exception as e:
            logging.error(f"Error calculating average prices: {str(e)}")
            return []

    @staticmethod
    def _build_query(origin_region_slugs: List[str], destination_region_slugs: List[str], origin: str, destination: str,
                     date_from: str, date_to: str):
        """
        Construct the SQL query based on the availability of slugs.

        Args:
            origin_region_slugs (List[str]): List of slugs for origin regions.
            destination_region_slugs (List[str]): List of slugs for destination regions.
            origin (str): Origin location slug.
            destination (str): Destination location slug.
            date_from (str): Start date for the price range.
            date_to (str): End date for the price range.

        Returns:
            Tuple[text, Dict[str, str]]: SQL query and corresponding parameters.
        """
        join_clause = ""
        where_clause = ""
        params = {"date_from": date_from, "date_to": date_to}

        if not origin_region_slugs and not destination_region_slugs:
            where_clause = "orig_code = :origin AND dest_code = :destination"
            params.update({"origin": origin, "destination": destination})
        elif not origin_region_slugs and destination_region_slugs:
            join_clause = "JOIN ports ON prices.dest_code = ports.code"
            where_clause = "orig_code = :origin AND ports.parent_slug IN :destination_slugs"
            params.update({"origin": origin, "destination_slugs": tuple(destination_region_slugs)})
        elif origin_region_slugs and not destination_region_slugs:
            join_clause = "JOIN ports ON prices.orig_code = ports.code"
            where_clause = "dest_code = :destination AND ports.parent_slug IN :origin_slugs"
            params.update({"destination": destination, "origin_slugs": tuple(origin_region_slugs)})
        else:
            join_clause = "JOIN ports p1 ON prices.orig_code = p1.code JOIN ports p2 ON prices.dest_code = p2.code"
            where_clause = "p1.parent_slug IN :origin_slugs AND p2.parent_slug IN :destination_slugs"
            params.update({"origin_slugs": tuple(origin_region_slugs), "destination_slugs": tuple(destination_region_slugs)})

        query = text(PriceService.BASE_QUERY.format(join_clause=join_clause, where_clause=where_clause))
        return query, params

    @staticmethod
    def _process_price_data(result) -> List[Dict[str, Optional[float]]]:
        """
        Convert the query result into the desired format.

        Args:
            result: The raw query result.

        Returns:
            List[Dict[str, Optional[float]]]: Processed list of dictionaries with day and average price.
        """
        return [
            {
                "day": day.strftime("%Y-%m-%d"),
                "average_price": None if avg_price is None or count < 3 else round(float(avg_price), 2)
            }
            for day, avg_price, count in result
        ]

class RegionService:
    BASE_QUERY = """
        SELECT slug FROM regions WHERE {condition}
    """

    @staticmethod
    def fetch_child_slugs(slug: str) -> List[str]:
        """
        Retrieve all child slugs for a given slug.

        Args:
            slug (str): Parent region slug.

        Returns:
            List[str]: List of child slugs including the given slug.
        """
        try:
            slugs = [slug]
            for current_slug in slugs:
                query, params = RegionService._build_query(current_slug, "parent_slug = :condition")
                result = db.session.execute(query, params)
                slugs.extend([row[0] for row in result])

            # Validate if the original slug exists in the database
            if len(slugs) == 1:
                validation_query, validation_params = RegionService._build_query(slug, "slug = :condition")
                result = db.session.execute(validation_query, validation_params)
                if result.fetchone() is None:
                    return []

            return slugs
        except Exception as e:
            logging.error(f"Error retrieving child slugs: {str(e)}")
            return []

    @staticmethod
    def _build_query(condition_value: str, condition: str):
        """
        Build the SQL query with the specified condition.

        Args:
            condition_value (str): Value for the condition in the query.
            condition (str): Condition string to format into the query.

        Returns:
            Tuple[text, Dict[str, str]]: SQL query and parameters.
        """
        query = text(RegionService.BASE_QUERY.format(condition=condition))
        params = {"condition": condition_value}
        return query, params

class ValidatePortService:
    @staticmethod
    def port_exists(port_code: str) -> bool:
        """
        Check if a port exists in the database.

        Returns:
            bool: True if the port exists, False otherwise.
        """
        try:
            result = db.session.execute(
                text("SELECT EXISTS(SELECT 1 FROM ports WHERE code = :code)"),
                {"code": port_code}
            ).scalar()
            return result
        except Exception as e:
            logging.error(f"Error checking if port exists: {str(e)}")
            return False

class ValidateSlugService:
    @staticmethod
    def slug_exists(slug: str) -> bool:
        """
        Check if a slug exists in the database.

        Returns:
            bool: True if the slug exists, False otherwise.
        """
        try:
            result = db.session.execute(
                text("SELECT EXISTS(SELECT 1 FROM regions WHERE slug = :slug)"),
                {"slug": slug}
            ).scalar()
            return result
        except Exception as e:
            logging.error(f"Error checking if slug exists: {str(e)}")
            return False

price_service = PriceService()
validate_port_service = ValidatePortService()
validate_slug_service = ValidateSlugService()