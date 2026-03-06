"""
app.py
Smart Laundry Operations Platform — Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import init_db, get_connection
from models import (
    add_outlet, get_all_outlets, get_outlet_count,
    add_order, get_order_by_id, get_orders_today_count,
    get_orders_by_outlet_today, get_orders_by_outlet_today_count,
    get_urgent_orders_by_outlet_count, get_ready_orders_by_outlet_count,
    get_in_process_count, get_ready_orders, get_ready_orders_by_area,
    update_order_status, authenticate_outlet,
    get_pending_batches, get_pending_batch_count, get_batch_order_count,
    get_or_create_available_batch, add_order_to_batch, start_processing_batch,
    generate_order_slip_pdf, get_analytics_service_type, get_analytics_status,
    get_analytics_outlet, get_analytics_delivery_area, get_delivery_metrics,
    get_overall_kpis, 
    add_driver, get_available_drivers, get_available_drivers_count, get_all_drivers, assign_driver_to_order, update_driver_status, get_driver_by_id
)


# ── Custom Styling ──────────────────────────────────────────────

def inject_custom_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        /* Dark Mode Base Styling */
        * { font-family: 'Outfit', sans-serif; }
        .stApp { 
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
        }
        
        /* Headers & Text */
        h1, h2, h3 { 
            color: #f1f5f9 !important; 
            font-weight: 700 !important; 
        }
        .stMarkdown p { 
            color: #cbd5e1 !important; 
        }

        /* Professional Metric Cards - Dark Mode */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid #334155 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            border-color: #4f46e5 !important;
        }
        .metric-label { 
            color: #94a3b8 !important; 
            font-size: 0.875rem; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.025em; 
        }
        .metric-value { 
            color: #f1f5f9 !important; 
            font-size: 1.875rem; 
            font-weight: 700; 
            margin: 0.25rem 0; 
        }
        
        /* Glassmorphism Containers - Dark */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            border-radius: 16px !important;
            border: 1px solid rgba(51, 65, 85, 0.8) !important;
            background: rgba(15, 23, 42, 0.8) !important;
            backdrop-filter: blur(8px);
            padding: 1.5rem !important;
        }

        /* Buttons - Dark Mode */
        .stButton button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: white !important;
            border: 1px solid #4f46e5 !important;
            border-radius: 10px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            opacity: 1 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.5) !important;
        }

        /* Tabs - Dark Mode */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            color: #94a3b8 !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e293b !important;
            color: #6366f1 !important;
            box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3) !important;
            border-bottom: 2px solid #6366f1 !important;
        }

        /* Badges - Dark Mode */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-ready { 
            background-color: rgba(34, 197, 94, 0.2) !important; 
            color: #86efac !important; 
            border: 1px solid #22c55e !important;
        }
        .badge-urgent { 
            background-color: rgba(239, 68, 68, 0.2) !important; 
            color: #fca5a5 !important; 
            border: 1px solid #ef4444 !important;
            animation: pulse 2s infinite; 
        }
        .badge-process { 
            background-color: rgba(59, 130, 246, 0.2) !important; 
            color: #93c5fd !important; 
            border: 1px solid #3b82f6 !important;
        }
        .badge-received { 
            background-color: rgba(148, 163, 184, 0.2) !important; 
            color: #cbd5e1 !important; 
            border: 1px solid #64748b !important;
        }

        /* Input Fields - Dark Mode */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select,
        .stNumberInput input {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
            border: 1px solid #334155 !important;
        }

        /* Form Container - Dark */
        .stForm {
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 20px !important;
        }

        /* Dividers - Dark */
        .stDivider {
            background-color: #334155 !important;
        }

        /* Info/Warning/Error Boxes - Dark */
        .stAlert {
            background-color: #1e293b !important;
            color: #e2e8f0 !important;
            border-left: 4px solid #6366f1 !important;
        }

        /* DataFrame - Dark */
        [data-testid="stDataFrame"] {
            background-color: #1e293b !important;
            color: #e2e8f0 !important;
        }

        /* Container Borders */
        .stContainer {
            border-color: #334155 !important;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

def metric_card(label, value, icon="📦"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def status_badge(status):
    cls = "badge-received"
    if status == "Ready": cls = "badge-ready"
    elif status == "In Process": cls = "badge-process"
    elif status == "Urgent": cls = "badge-urgent"
    
    return f'<span class="badge {cls}">{status}</span>'

# ── Page Config ─────────────────────────────────────────────────

st.set_page_config(
    page_title="Smart Laundry Operations Platform",
    page_icon="🧺",
    layout="wide",
)

init_db()

# ── Session State Defaults ──────────────────────────────────────

if "role" not in st.session_state:
    st.session_state.role = None
if "outlet_name" not in st.session_state:
    st.session_state.outlet_name = None
if "last_order_id" not in st.session_state:
    st.session_state.last_order_id = None


# ── Helper: Logout ──────────────────────────────────────────────

def show_logout():
    with st.sidebar:
        st.markdown(f"**Role:** {st.session_state.role}")
        if st.session_state.outlet_name:
            st.markdown(f"**Outlet:** {st.session_state.outlet_name}")
        if st.button("🔓 Logout"):
            st.session_state.role = None
            st.session_state.outlet_name = None
            st.session_state.last_order_id = None
            st.rerun()


# ════════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ════════════════════════════════════════════════════════════════

def login_screen():
    st.markdown(
        "<h1 style='text-align:center; margin-bottom: 0; color: #f1f5f9;'>🧺 Smart Laundry</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#94a3b8; font-size: 1.1rem;'>Premium Operations & Logistics Platform</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 👑 Owner", help=None)
            st.caption("Strategic oversight & branch analytics")
            if st.button("Access Dashboard", key="owner_login", use_container_width=True):
                st.session_state.role = "Owner"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🏪 Outlet", help=None)
            st.caption("Order processing & management")
            if st.button("Staff Portal", key="outlet_login", use_container_width=True):
                st.session_state.role = "Outlet Login"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### 🚚 Delivery", help=None)
            st.caption("Logistics & order fulfilment")
            if st.button("Driver View", key="delivery_login", use_container_width=True):
                st.session_state.role = "Delivery"
                st.rerun()


# ════════════════════════════════════════════════════════════════
# OUTLET LOGIN FORM
# ════════════════════════════════════════════════════════════════

def outlet_login_form():
    st.markdown(
        "<h1 style='text-align:center; color: #f1f5f9;'>🏪 Outlet Staff Login</h1>",
        unsafe_allow_html=True,
    )
    st.divider()

    with st.form("outlet_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if username and password:
                outlet = authenticate_outlet(username, password)
                if outlet:
                    st.session_state.role = "Outlet"
                    st.session_state.outlet_name = outlet["outlet_name"]
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter both username and password.")

    if st.button("← Back to Login"):
        st.session_state.role = None
        st.rerun()


# ════════════════════════════════════════════════════════════════
# OWNER DASHBOARD
# ════════════════════════════════════════════════════════════════

def owner_dashboard():
    show_logout()
    st.title("👑 Owner Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📊 Analytics Overview", "🏪 Outlet Management", "➕ Operations"])

    # ── Branch Filter for Analytics
    outlets_list = get_all_outlets()
    outlet_names = ["Overall"] + [o["outlet_name"] for o in outlets_list]
    
    with tab1:
        c_filter1, c_filter2 = st.columns([2, 1])
        selected_filter = c_filter1.selectbox("🎯 Select Branch Filter", outlet_names, label_visibility="collapsed")
        outlet_filter = None if selected_filter == "Overall" else selected_filter

        # ── KPI Metrics
        kpis = get_overall_kpis(outlet_filter)
        st.markdown(f"#### 📈 {selected_filter} Performance")
        m1, m2, m3, m4 = st.columns(4)
        with m1: metric_card("Total Orders", kpis["total"], "📦")
        with m2: metric_card("Urgent", kpis["urgent"], "⚡")
        with m3: metric_card("In Process", kpis["in_process"], "🔄")
        with m4: metric_card("Ready", kpis["ready"], "✅")

        # ── Extended KPIs
        st.markdown("#### 📊 Extended Metrics")
        conn = get_connection()
        today = date.today().isoformat()
        
        # Get additional metrics
        base_filter = "" if outlet_filter is None else f" AND outlet_name = '{outlet_filter}'"
        delivered_count = conn.execute(f"SELECT COUNT(*) FROM orders WHERE DATE(created_at) = '{today}' AND status = 'Delivered'{base_filter}").fetchone()[0]
        delivery_count = conn.execute(f"SELECT COUNT(*) FROM orders WHERE DATE(created_at) = '{today}' AND order_type = 'Delivery'{base_filter}").fetchone()[0]
        pickup_count = conn.execute(f"SELECT COUNT(*) FROM orders WHERE DATE(created_at) = '{today}' AND order_type = 'Pickup'{base_filter}").fetchone()[0]
        received_count = conn.execute(f"SELECT COUNT(*) FROM orders WHERE DATE(created_at) = '{today}' AND status = 'Received'{base_filter}").fetchone()[0]
        avg_items_result = conn.execute(f"SELECT ROUND(AVG(items), 1) FROM orders WHERE DATE(created_at) = '{today}'{base_filter}").fetchone()[0]
        conn.close()
        
        avg_items = avg_items_result if avg_items_result else 0
        
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        with k1: metric_card("Delivered", delivered_count, "✔️")
        with k2: metric_card("For Delivery", delivery_count, "🚚")
        with k3: metric_card("For Pickup", pickup_count, "🏪")
        with k4: metric_card("Received", received_count, "📥")
        with k5: 
            completion_rate = round((delivered_count / kpis["total"] * 100) if kpis["total"] > 0 else 0)
            metric_card("Completion %", f"{completion_rate}%", "📈")
        with k6:
            metric_card("Avg Items/Order", f"{avg_items}", "📦")

        st.divider()

        # ── Analytics (Charts)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 🧺 Service Distribution")
            svc_data = get_analytics_service_type(outlet_filter)
            if svc_data:
                df_svc = pd.DataFrame(svc_data)
                fig_svc = px.bar(df_svc, x='service_type', y='count', color='service_type', 
                               template="plotly_white")
                fig_svc.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), 
                                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='#e2e8f0'))
                st.plotly_chart(fig_svc, use_container_width=True)
            else:
                st.info("No service data available.")

        with c2:
            st.markdown("##### 🏷️ Order Status")
            status_data = get_analytics_status(outlet_filter)
            if status_data:
                df_status = pd.DataFrame(status_data)
                fig_status = px.pie(df_status, values='count', names='status', hole=0.5,
                                  color_discrete_sequence=px.colors.qualitative.Set2)
                fig_status.update_layout(margin=dict(t=0, b=0, l=0, r=0),
                                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                        font=dict(color='#e2e8f0'))
                st.plotly_chart(fig_status, use_container_width=True)
            else:
                st.info("No status data available.")

        # ── Additional Analytics
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("##### 🗺️ Delivery Area Performance")
            area_data = get_analytics_delivery_area(outlet_filter)
            if area_data:
                df_area = pd.DataFrame(area_data)
                fig_area = px.bar(df_area, x='delivery_area', y='count', color='delivery_area',
                                template="plotly_white")
                fig_area.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
                                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                      font=dict(color='#e2e8f0'))
                st.plotly_chart(fig_area, use_container_width=True)
            else:
                st.info("No area data available.")

        with c4:
            st.markdown("##### 🏢 Outlet Performance")
            if outlet_filter is None:
                outlet_data = get_analytics_outlet()
                if outlet_data:
                    df_outlet = pd.DataFrame(outlet_data)
                    fig_outlet = px.bar(df_outlet, x='outlet_name', y='count', color='outlet_name',
                                      template="plotly_white")
                    fig_outlet.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
                                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                            font=dict(color='#e2e8f0'), xaxis_tickangle=-45)
                    st.plotly_chart(fig_outlet, use_container_width=True)
                else:
                    st.info("No outlet data available.")
            else:
                st.info("Select 'Overall' to see outlet comparison.")

    with tab2:
        st.subheader("🏪 Registered Outlets")
        outlets = get_all_outlets()
        if outlets:
            df = pd.DataFrame(outlets)
            df = df[["id", "outlet_name", "location", "username", "created_at"]]
            df.columns = ["ID", "Outlet Name", "Location", "Username", "Joined"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("➕ Register New Outlet")
        with st.form("create_outlet_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            oname = f1.text_input("Outlet Name", placeholder="e.g. Downtown Branch")
            loc = f2.text_input("Location", placeholder="e.g. Pune, MH")
            f3, f4 = st.columns(2)
            uname = f3.text_input("System Username")
            pword = f4.text_input("System Password", type="password")

            if st.form_submit_button("Create Outlet Account"):
                if oname and loc and uname and pword:
                    try:
                        add_outlet(oname, loc, uname, pword)
                        st.success(f"Successfully registered {oname}")
                        st.rerun()
                    except Exception:
                        st.error("Registration failed. Username might be taken.")
                else:
                    st.warning("Please complete all registration fields.")

    with tab3:
        st.info("More owner operations coming soon...")


# ════════════════════════════════════════════════════════════════
# OUTLET DASHBOARD
# ════════════════════════════════════════════════════════════════

def outlet_dashboard():
    show_logout()
    outlet_name = st.session_state.outlet_name
    st.title(f"🏪 {outlet_name} Portal")
    
    tab1, tab2 = st.tabs(["📊 Performance Overview", "📝 Order Management"])

    with tab1:
        # ── Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: metric_card("Today's Orders", get_orders_by_outlet_today_count(outlet_name), "📦")
        with m2: metric_card("Urgent", get_urgent_orders_by_outlet_count(outlet_name), "⚡")
        with m3: metric_card("Ready", get_ready_orders_by_outlet_count(outlet_name), "✅")
        with m4: metric_card("Batches", get_pending_batch_count(outlet_name), "📋")
        with m5: metric_card("Available Drivers", get_available_drivers_count(), "🚚")

        st.divider()

        # ── Create Order
        with st.expander("➕ Create New Order", expanded=False):
            with st.form("create_order_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                customer_name = c1.text_input("Customer Name", placeholder="John Doe")
                phone = c2.text_input("Phone Number", placeholder="+91 ...")

                c3, c4, c5, c6 = st.columns(4)
                service_type = c3.selectbox("Service", ["Wash & Fold", "Wash & Iron", "Iron Only", "Dry Cleaning"])
                service_mode = c4.selectbox("Priority", ["Regular", "Urgent"])
                delivery_area = c5.selectbox("Area", ["Baner", "Wakad", "Aundh", "Hinjewadi", "Pashan"])
                order_type = c6.selectbox("Type", ["Delivery", "Pickup"])

                st.markdown("**Clothing Breakdown**")
                ic1, ic2, ic3, ic4, ic5 = st.columns(5)
                shirts = ic1.number_input("Shirts", min_value=0, step=1)
                jeans = ic2.number_input("Jeans", min_value=0, step=1)
                dresses = ic3.number_input("Dresses", min_value=0, step=1)
                traditional = ic4.number_input("Traditional", min_value=0, step=1)
                others = ic5.number_input("Misc", min_value=0, step=1)

                total_display = shirts + jeans + dresses + traditional + others
                if st.form_submit_button("Submit Order", use_container_width=True):
                    if customer_name and phone and total_display > 0:
                        order_id = add_order(customer_name, phone, service_type, service_mode,
                                           shirts, jeans, dresses, traditional, others, outlet_name, delivery_area, order_type)
                        st.session_state.last_order_id = order_id
                        st.success(f"Order #{order_id} recorded!")
                        st.rerun()
                    else:
                        st.warning("Incomplete order details.")

    with tab2:
        st.subheader("📋 Active Orders")
        orders = get_orders_by_outlet_today(outlet_name)
        if orders:
            for order in orders:
                with st.container(border=True):
                    # Top row with order info
                    c1, c2, c3, c4 = st.columns([1, 2, 2, 1.5])
                    
                    with c1:
                        st.markdown(f"**#{order['id']}**")
                        st.caption("🚚" if order.get('order_type')=='Delivery' else "🏪")
                    
                    with c2:
                        st.markdown(f"**{order['customer_name']}**")
                        st.caption(f"📍 {order['delivery_area']}")
                    
                    with c3:
                        st.markdown(f"{order['service_type']}")
                        st.markdown(status_badge(order['status']) if order['service_mode'] == 'Regular' else status_badge('Urgent'), unsafe_allow_html=True)
                        if order['service_mode'] == 'Urgent' and order['status'] != 'Ready':
                             st.markdown(status_badge(order['status']), unsafe_allow_html=True)

                    with c4:
                        if order["status"] == "Received":
                            col_a, col_b = st.columns(2)
                            if col_a.button("⚙️", key=f"p_{order['id']}", help="Process"):
                                update_order_status(order["id"], "In Process"); st.rerun()
                            if col_b.button("📋", key=f"b_{order['id']}", help="Batch"):
                                bid, bname = get_or_create_available_batch(outlet_name)
                                add_order_to_batch(order["id"], bid); st.rerun()
                        elif order["status"] == "In Process":
                            if st.button("Mark Ready", key=f"r_{order['id']}", use_container_width=True):
                                update_order_status(order["id"], "Ready"); st.rerun()
                        elif order["status"] == "Ready":
                            if order.get('order_type') == 'Delivery' and not order.get('driver_id'):
                                # Show driver assignment option
                                available_drivers = get_available_drivers()
                                if available_drivers:
                                    driver_options = {d['id']: f"{d['driver_name']} ({d['phone']})" for d in available_drivers}
                                    selected_driver_id = st.selectbox(f"Assign Driver", options=list(driver_options.keys()), format_func=lambda x: driver_options[x], key=f"driver_{order['id']}")
                                    if st.button(f"✓ Assign", key=f"assign_{order['id']}", use_container_width=True):
                                        assign_driver_to_order(order['id'], selected_driver_id)
                                        st.success("Driver assigned!")
                                        st.rerun()
                                else:
                                    st.warning("No drivers available")
                            elif order.get('driver_id'):
                                driver = get_driver_by_id(order['driver_id'])
                                if driver:
                                    st.info(f"🚚 Driver: {driver['driver_name']}")
                            else:
                                st.success("Notified 📱")
                    
                    # Second row with slip download
                    st.divider()
                    dl_col1, dl_col2 = st.columns([1, 5])
                    with dl_col1:
                        pdf_bytes = generate_order_slip_pdf(order)
                        st.download_button(
                            label="📄 Slip", 
                            data=pdf_bytes, 
                            file_name=f"order_{order['id']}.pdf", 
                            mime="application/pdf",
                            key=f"slip_{order['id']}"
                        )
                    with dl_col2:
                        st.caption(f"Created: {order['created_at'][:10] if order.get('created_at') else 'N/A'} | Items: {order.get('items', 0)}")
        else:
            st.info("No active orders for today.")

        st.divider()
        st.subheader("📋 Batch Tracking")
        batches = get_pending_batches(outlet_name)
        if batches:
            for batch in batches:
                order_count = get_batch_order_count(batch["id"])
                with st.container(border=True):
                    bc1, bc2, bc3 = st.columns([2, 1, 1.5])
                    bc1.markdown(f"**{batch['batch_name']}**")
                    bc2.markdown(f"📦 {order_count} Items")
                    if order_count > 0:
                        if bc3.button("Process Batch", key=f"sb_{batch['id']}"):
                            start_processing_batch(batch["id"]); st.rerun()


# ════════════════════════════════════════════════════════════════
# DELIVERY DASHBOARD
# ════════════════════════════════════════════════════════════════

def delivery_dashboard():
    show_logout()
    st.title("🚚 Delivery Staff Dashboard")
    
    tab1, tab2 = st.tabs(["📦 Deliveries", "➕ Add Driver"])
    
    with tab1:
        st.divider()

        # ── Metrics
        metrics = get_delivery_metrics()
        m1, m2, m3 = st.columns(3)
        m1.metric("✅ Today's Deliveries", metrics["delivered"])
        m2.metric("📦 Pending Deliveries", metrics["pending"])
        m3.metric("📍 Areas Covered Today", metrics["areas"])

        st.divider()

        # ── Ready Orders Grouped by Area
        st.subheader("📦 Orders Ready for Delivery (by Area)")
        grouped_orders = get_ready_orders_by_area()
        
        if grouped_orders:
            for area, orders in grouped_orders.items():
                with st.expander(f"📍 {area} ({len(orders)} orders)", expanded=True):
                    for order in orders:
                        with st.container(border=True):
                            c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
                            c1.write(f"**#{order['id']}**\n\n🏪 {order['outlet_name']}")
                            c2.write(f"👤 {order['customer_name']}\n\n📞 {order['phone']}")
                            
                            # Show driver info if assigned
                            driver_info = ""
                            if order.get('driver_name'):
                                driver_info = f"\n🚚 {order['driver_name']} ({order['driver_phone']})"
                            
                            c3.write(f"🧺 {order['service_type']}{driver_info}")
                            
                            if c4.button("✅ Delivered", key=f"deliver_{order['id']}"):
                                update_order_status(order["id"], "Delivered")
                                # Mark driver as available again
                                if order.get('driver_id'):
                                    update_driver_status(order['driver_id'], 'Available')
                                    st.success(f"Driver marked as available!")
                                st.rerun()
        else:
            st.info("No orders ready for delivery right now.")
    
    with tab2:
        st.subheader("➕ Register New Driver")
        st.markdown("Add a new delivery driver to the system")
        st.divider()
        
        with st.form("add_driver_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            driver_name = c1.text_input("Driver Name", placeholder="e.g. Ramesh Kumar")
            phone = c2.text_input("Phone Number", placeholder="+91 or 10-digit number")
            
            c3, c4 = st.columns(2)
            vehicle_type = c3.selectbox("Vehicle Type", ["Two-wheeler", "Auto", "Car", "Van"])
            vehicle_number = c4.text_input("Vehicle Number", placeholder="e.g. MH02AB1234")
            
            delivery_area = st.selectbox("Delivery Area", ["Baner", "Wakad", "Aundh", "Hinjewadi", "Pashan"])
            
            if st.form_submit_button("Register Driver", use_container_width=True):
                if driver_name and phone and vehicle_number:
                    try:
                        driver_id = add_driver(driver_name, phone, vehicle_type, vehicle_number, delivery_area)
                        st.success(f"✅ Driver registered successfully! ID: {driver_id}")
                        st.rerun()
                    except Exception as e:
                        if "UNIQUE constraint failed" in str(e):
                            st.error("❌ This phone number is already registered")
                        else:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please fill in all required fields")
        
        st.divider()
        st.subheader("👥 Active Drivers")
        drivers = get_all_drivers()
        
        if drivers:
            with st.expander(f"View All {len(drivers)} Drivers", expanded=True):
                for driver in drivers:
                    with st.container(border=True):
                        dc1, dc2, dc3, dc4 = st.columns([2, 2, 1.5, 1])
                        
                        dc1.markdown(f"**{driver['driver_name']}**")
                        dc1.caption(f"📞 {driver['phone']}")
                        
                        dc2.markdown(f"🚗 {driver['vehicle_type']}")
                        dc2.caption(f"📋 {driver['vehicle_number']}")
                        
                        dc3.markdown(f"📍 {driver['delivery_area']}")
                        
                        status_color = "🟢" if driver['status'] == 'Available' else "🔴"
                        dc4.markdown(f"{status_color} {driver['status']}")
        else:
            st.info("No drivers registered yet. Add one above!")


# ════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ════════════════════════════════════════════════════════════════

def main():
    inject_custom_css()
    role = st.session_state.role

    if role is None:
        login_screen()
    elif role == "Owner":
        owner_dashboard()
    elif role == "Outlet Login":
        outlet_login_form()
    elif role == "Outlet":
        outlet_dashboard()
    elif role == "Delivery":
        delivery_dashboard()


if __name__ == "__main__":
    main()
