"""
models.py
CRUD helper functions for outlets, orders, and batches.
"""

from database import get_connection
from datetime import date, datetime
import io
import requests
import urllib.parse
import os

# ── Outlet Helpers ──────────────────────────────────────────────

def add_outlet(outlet_name, location, username, password):
    """Create a new outlet with login credentials."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO outlets (outlet_name, location, username, password) VALUES (?, ?, ?, ?)",
        (outlet_name, location, username, password),
    )
    conn.commit()
    conn.close()



def get_all_outlets():
    """Return all outlets as a list of dicts."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM outlets ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_outlet_count():
    """Return total number of outlets."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM outlets").fetchone()[0]
    conn.close()
    return count


def authenticate_outlet(username, password):
    """Verify outlet credentials. Returns outlet dict or None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM outlets WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Driver Helpers ──────────────────────────────────────────────

def add_driver(driver_name, phone, vehicle_type, vehicle_number, delivery_area):
    """Create a new driver account."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO drivers (driver_name, phone, vehicle_type, vehicle_number, delivery_area, status) VALUES (?, ?, ?, ?, ?, 'Available')",
            (driver_name, phone, vehicle_type, vehicle_number, delivery_area),
        )
        conn.commit()
        driver_id = cursor.lastrowid
        conn.close()
        return driver_id
    except Exception as e:
        conn.close()
        raise e


def get_available_drivers():
    """Return all available drivers."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM drivers WHERE status = 'Available' ORDER BY driver_name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_drivers():
    """Return all drivers."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM drivers ORDER BY driver_name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_available_drivers_count():
    """Count available drivers."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM drivers WHERE status = 'Available'").fetchone()[0]
    conn.close()
    return count


def assign_driver_to_order(order_id, driver_id):
    """Assign a driver to a delivery order."""
    conn = get_connection()
    conn.execute("UPDATE orders SET driver_id = ? WHERE id = ?", (driver_id, order_id))
    conn.execute("UPDATE drivers SET status = 'On Delivery' WHERE id = ?", (driver_id,))
    conn.commit()
    conn.close()


def update_driver_status(driver_id, new_status):
    """Update driver status (Available, On Delivery, Offline)."""
    conn = get_connection()
    conn.execute("UPDATE drivers SET status = ? WHERE id = ?", (new_status, driver_id))
    conn.commit()
    conn.close()


def get_driver_by_id(driver_id):
    """Get driver details by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM drivers WHERE id = ?", (driver_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Order Helpers ───────────────────────────────────────────────

def add_order(customer_name, phone, service_type, service_mode,
              shirts, jeans, dresses, traditional, others, outlet_name, delivery_area, order_type):
    """Create a new order with clothing breakdown, delivery area, and order type."""
    total_items = shirts + jeans + dresses + traditional + others
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO orders
           (customer_name, phone, service_type, service_mode, delivery_area, order_type,
            shirts, jeans, dresses, traditional, others, items,
            outlet_name, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Received')""",
        (customer_name, phone, service_type, service_mode, delivery_area, order_type,
         shirts, jeans, dresses, traditional, others, total_items, outlet_name),
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


def get_order_by_id(order_id):
    """Return a single order by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_orders_today_count():
    """Count of today's orders."""
    conn = get_connection()
    today = date.today().isoformat()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ?", (today,)
    ).fetchone()[0]
    conn.close()
    return count


def get_orders_by_outlet_today(outlet_name):
    """Return today's orders for a specific outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    rows = conn.execute(
        "SELECT * FROM orders WHERE DATE(created_at) = ? AND outlet_name = ? ORDER BY created_at DESC",
        (today, outlet_name),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_orders_by_outlet_today_count(outlet_name):
    """Count of today's orders for a specific outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ? AND outlet_name = ?",
        (today, outlet_name),
    ).fetchone()[0]
    conn.close()
    return count


def get_urgent_orders_by_outlet_count(outlet_name):
    """Count of today's urgent orders for a specific outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ? AND outlet_name = ? AND service_mode = 'Urgent'",
        (today, outlet_name),
    ).fetchone()[0]
    conn.close()
    return count


def get_ready_orders_by_outlet_count(outlet_name):
    """Count of today's ready orders for a specific outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ? AND outlet_name = ? AND status = 'Ready'",
        (today, outlet_name),
    ).fetchone()[0]
    conn.close()
    return count


def get_in_process_count():
    """Count of today's orders with status 'In Process'."""
    conn = get_connection()
    today = date.today().isoformat()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ? AND status = 'In Process'",
        (today,),
    ).fetchone()[0]
    conn.close()
    return count


def get_ready_orders():
    """Return all orders with status 'Ready' and type 'Delivery'."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM orders WHERE status = 'Ready' AND order_type = 'Delivery' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_ready_orders_by_area():
    """Return ready orders (Delivery only) grouped by area with driver info."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT o.*, o.driver_id, d.driver_name, d.phone as driver_phone, d.vehicle_type, d.vehicle_number
        FROM orders o
        LEFT JOIN drivers d ON o.driver_id = d.id
        WHERE o.status = 'Ready' AND o.order_type = 'Delivery'
        ORDER BY o.delivery_area, o.created_at DESC
    """).fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        area = row['delivery_area'] or "Unknown"
        if area not in grouped:
            grouped[area] = []
        grouped[area].append(dict(row))
    return grouped


def update_order_status(order_id, new_status):
    """Update the status of an order."""
    conn = get_connection()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()


# ── Batch Helpers ───────────────────────────────────────────────

def create_batch(outlet_name):
    """Create a new batch for an outlet."""
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM batches WHERE outlet_name = ?", (outlet_name,)
    ).fetchone()[0]
    letter = chr(65 + (count % 26))
    batch_name = f"Batch {letter}"
    cursor = conn.execute(
        "INSERT INTO batches (batch_name, outlet_name, status) VALUES (?, ?, 'Pending')",
        (batch_name, outlet_name),
    )
    batch_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return batch_id, batch_name


def get_pending_batches(outlet_name):
    """Return pending batches for an outlet."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM batches WHERE outlet_name = ? AND status = 'Pending' ORDER BY created_at DESC",
        (outlet_name,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_pending_batch_count(outlet_name):
    """Count of pending batches for an outlet."""
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM batches WHERE outlet_name = ? AND status = 'Pending'",
        (outlet_name,),
    ).fetchone()[0]
    conn.close()
    return count


def get_batch_order_count(batch_id):
    """Count orders in a batch."""
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE batch_id = ?", (batch_id,)
    ).fetchone()[0]
    conn.close()
    return count


def add_order_to_batch(order_id, batch_id):
    """Assign an order to a batch."""
    conn = get_connection()
    conn.execute("UPDATE orders SET batch_id = ? WHERE id = ?", (batch_id, order_id))
    conn.commit()
    conn.close()


def get_or_create_available_batch(outlet_name):
    """Get an existing pending batch or create a new one."""
    batches = get_pending_batches(outlet_name)
    for batch in batches:
        if get_batch_order_count(batch["id"]) < 10:
            return batch["id"], batch["batch_name"]
    return create_batch(outlet_name)


def start_processing_batch(batch_id):
    """Mark batch orders as 'In Process'."""
    conn = get_connection()
    conn.execute("UPDATE orders SET status = 'In Process' WHERE batch_id = ?", (batch_id,))
    conn.execute("UPDATE batches SET status = 'Processing' WHERE id = ?", (batch_id,))
    conn.commit()
    conn.close()


# ── Analytics Helpers (Owner Dashboard) ──────────────────────────

def get_analytics_service_type(outlet_filter=None):
    """Counts of today's orders by service type, optionally filtered by outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    query = "SELECT service_type, COUNT(*) as count FROM orders WHERE DATE(created_at) = ?"
    params = [today]
    if outlet_filter:
        query += " AND outlet_name = ?"
        params.append(outlet_filter)
    query += " GROUP BY service_type"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_analytics_status(outlet_filter=None):
    """Counts of today's orders by status, optionally filtered by outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    query = "SELECT status, COUNT(*) as count FROM orders WHERE DATE(created_at) = ?"
    params = [today]
    if outlet_filter:
        query += " AND outlet_name = ?"
        params.append(outlet_filter)
    query += " GROUP BY status"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_analytics_outlet():
    """Counts of today's orders by outlet (always overall)."""
    conn = get_connection()
    today = date.today().isoformat()
    rows = conn.execute(
        "SELECT outlet_name, COUNT(*) as count FROM orders WHERE DATE(created_at) = ? GROUP BY outlet_name",
        (today,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_analytics_delivery_area(outlet_filter=None):
    """Counts of today's orders by delivery area, optionally filtered by outlet."""
    conn = get_connection()
    today = date.today().isoformat()
    query = "SELECT delivery_area, COUNT(*) as count FROM orders WHERE DATE(created_at) = ?"
    params = [today]
    if outlet_filter:
        query += " AND outlet_name = ?"
        params.append(outlet_filter)
    query += " GROUP BY delivery_area"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_overall_kpis(outlet_filter=None):
    """KPI counts for total orders, urgent orders, and in-process orders."""
    conn = get_connection()
    today = date.today().isoformat()
    
    base_query = "WHERE DATE(created_at) = ?"
    params = [today]
    if outlet_filter:
        base_query += " AND outlet_name = ?"
        params.append(outlet_filter)

    total_orders = conn.execute(f"SELECT COUNT(*) FROM orders {base_query}", params).fetchone()[0]
    urgent_orders = conn.execute(f"SELECT COUNT(*) FROM orders {base_query} AND service_mode = 'Urgent'", params).fetchone()[0]
    in_process = conn.execute(f"SELECT COUNT(*) FROM orders {base_query} AND status = 'In Process'", params).fetchone()[0]
    ready_orders = conn.execute(f"SELECT COUNT(*) FROM orders {base_query} AND status = 'Ready'", params).fetchone()[0]
    
    conn.close()
    return {
        "total": total_orders,
        "urgent": urgent_orders,
        "in_process": in_process,
        "ready": ready_orders
    }


def get_delivery_metrics():
    """Summary of today's deliveries."""
    conn = get_connection()
    today = date.today().isoformat()
    
    today_delivered = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = ? AND status = 'Delivered'", (today,)
    ).fetchone()[0]
    
    pending_deliveries = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'Ready'"
    ).fetchone()[0]
    
    areas_covered = conn.execute(
        "SELECT COUNT(DISTINCT delivery_area) FROM orders WHERE DATE(created_at) = ? AND status = 'Delivered'", (today,)
    ).fetchone()[0]
    
    conn.close()
    return {
        "delivered": today_delivered,
        "pending": pending_deliveries,
        "areas": areas_covered
    }


# ── PDF Slip Generation ────────────────────────────────────────

def generate_order_slip_pdf(order):
    """Generate a small receipt-style PDF for an order."""
    try:
        from fpdf import FPDF
        from io import BytesIO
        
        # Create a BytesIO buffer to capture PDF output
        pdf_buffer = BytesIO()
        
        # Create PDF with proper settings
        pdf = FPDF(unit="mm", format=(80, 200), orientation="P")
        pdf.add_page()
        pdf.set_margins(5, 5, 5)
        pdf.set_auto_page_break(auto=False)
        
        # Title
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, "SMART LAUNDRY", ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 4, "-" * 40, ln=True, align="C")
        pdf.ln(1)
        
        # Order details
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 4, f"Order ID: {order.get('id', 'N/A')}", ln=True)
        
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 4, f"Customer: {order.get('customer_name', 'N/A')}", ln=True)
        pdf.cell(0, 4, f"Phone: {order.get('phone', 'N/A')}", ln=True)
        pdf.cell(0, 4, f"Area: {order.get('delivery_area', 'N/A')}", ln=True)
        pdf.cell(0, 4, f"Outlet: {order.get('outlet_name', 'N/A')}", ln=True)
        pdf.ln(1)
        
        pdf.cell(0, 4, f"Service: {order.get('service_type', 'N/A')}", ln=True)
        pdf.cell(0, 4, f"Mode: {order.get('service_mode', 'N/A')}", ln=True)
        pdf.cell(0, 4, f"Type: {order.get('order_type', 'Delivery')}", ln=True)
        pdf.ln(1)
        
        # Items
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 4, "Items:", ln=True)
        pdf.set_font("Helvetica", "", 8)
        
        items_list = [
            ("Shirts", order.get("shirts", 0)),
            ("Jeans", order.get("jeans", 0)),
            ("Dresses", order.get("dresses", 0)),
            ("Traditional", order.get("traditional", 0)),
            ("Others", order.get("others", 0)),
        ]
        
        for item_name, qty in items_list:
            if qty > 0:
                pdf.cell(30, 4, f"  {item_name}:", ln=False)
                pdf.cell(0, 4, f"x{qty}", ln=True)
        
        pdf.ln(1)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 4, f"Total: {order.get('items', 0)} items", ln=True)
        
        # Footer
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 7)
        
        order_date = order.get("created_at", "")
        if order_date:
            try:
                dt = datetime.fromisoformat(str(order_date))
                order_date = dt.strftime("%Y-%m-%d")
            except:
                order_date = str(order_date)[:10] if order_date else "N/A"
        else:
            order_date = "N/A"
        
        pdf.cell(0, 3, f"Date: {order_date}", ln=True, align="C")
        pdf.cell(0, 3, "-" * 40, ln=True, align="C")
        
        # Output PDF - handle different return types
        pdf_output = pdf.output()
        
        # Convert to bytes
        if isinstance(pdf_output, bytes):
            return pdf_output
        elif isinstance(pdf_output, bytearray):
            return bytes(pdf_output)
        elif isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        else:
            return b""
        
    except Exception as e:
        print(f"⚠️ PDF Generation Error: {e}")
        import traceback
        traceback.print_exc()
        return b""
