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
        """Calculate average prices based on origin and destination."""
        try:
            region_service = RegionService()
            origin_region_slugs = region_service.fetch_child_slugs(origin)
            destination_region_slugs = region_service.fetch_child_slugs(destination)

            query, params = PriceService._build_query(origin_region_slugs, destination_region_slugs, origin, destination, date_from,
                                                      date_to)
            result = db.session.execute(query, params)

            return PriceService._process_price_data(result)
        except Exception as e:
            logging.error(f"Error calculating average prices: {str(e)}")
            return []

    @staticmethod
    def _build_query(origin_region_slugs: List[str], destination_region_slugs: List[str], origin: str, destination: str,
                     date_from: str, date_to: str):
        """Build the appropriate SQL query based on slug availability."""
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
        """Process the query results into the required format."""
        return [
            {
                "day": day.strftime("%Y-%m-%d"),
                "average_price": round(float(avg_price), 2) if avg_price is not None and count >= 3 else None
            }
            for day, avg_price, count in result
        ]

class RegionService:
    BASE_QUERY = """
            SELECT slug FROM regions WHERE {condition}
        """

    @staticmethod
    def fetch_child_slugs(slug: str) -> List[str]:
        """Retrieve all child slugs for a given slug."""

        try:
            slugs = [slug]
            for current_slug in slugs:
                query, params = RegionService._build_query(current_slug, "parent_slug = :condition")
                result = db.session.execute(query, params)
                slugs.extend(
                    [row[0] for row in result]
                )

            # Validate if the input slug exists
            if slugs and len(slugs[0]) >= 0 and len(slugs) == 1:
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
        """Build the SQL query with the appropriate condition."""
        query = text(RegionService.BASE_QUERY.format(condition=condition))
        params = {"condition": condition_value}
        return query, params

price_service = PriceService()