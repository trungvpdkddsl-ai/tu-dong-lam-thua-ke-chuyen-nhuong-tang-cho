import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
import io
from datetime import datetime

st.set_page_config(page_title="Tạo Hồ Sơ Thừa Kế - Phú Thọ", layout="wide")

st.title("⚖️ Công cụ Tạo Hồ Sơ Thừa Kế & Đất Đai")
st.info("Hỗ trợ tự động điền mẫu đơn cho khu vực xã Dân Chủ, huyện Phù Ninh.")

# --- PHẦN 1: THÔNG TIN VĂN BẢN ---
col_date1, col_date2 = st.columns(2)
with col_date1:
    ngay_lap = st.text_input("Ngày lập văn bản (Ví dụ: 09/02/2026)", value=datetime.now().strftime("%d/%m/%2026"))
with col_date2:
    so_gcn = st.text_input("Số phát hành GCN QSDĐ", value="00457H QSDĐ")

# --- PHẦN 2: THÔNG TIN NGƯỜI KHAI ---
with st.expander("👤 Thông tin Người khai / Người làm đơn", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        ho_ten_khai = st.text_input("Họ tên người khai", value="Hán Nghị Quyết")
        nam_sinh_khai = st.text_input("Năm sinh người khai", value="1935")
    with c2:
        cccd_khai = st.text_input("Số CCCD người khai", value="025035000185")
        ngay_cap_khai = st.text_input("Ngày cấp CCCD", value="29/04/2021")
    with c3:
        dia_chi_khai = st.text_input("Địa chỉ thường trú", value="Khu 6, xã Dân Chủ, tỉnh Phú Thọ")

# --- PHẦN 3: THÀNH VIÊN HỘ GIA ĐÌNH ---
st.subheader("👥 Danh sách thành viên hộ gia đình (tại thời điểm cấp đất)")
st.caption("Bạn có thể thêm/bớt hàng trực tiếp trên bảng này.")

# Dữ liệu mặc định từ file của bạn
df_default = pd.DataFrame([
    {"ho_ten": "Hán Nghị Quyết", "nam_sinh": "1948", "quan_he": "Chủ hộ", "cccd": "025035000185"},
    {"ho_ten": "Nguyễn Thị Đạo", "nam_sinh": "1934", "quan_he": "Vợ chủ hộ", "cccd": "025134002289"},
    {"ho_ten": "Hán Thanh Hòa", "nam_sinh": "1973", "quan_he": "Con chủ hộ", "cccd": "025073003619"},
    {"ho_ten": "Hán Thị Sinh", "nam_sinh": "1977", "quan_he": "Con chủ hộ", "cccd": "025177004355"},
    {"ho_ten": "Hán Đức Bình", "nam_sinh": "1973", "quan_he": "Con chủ hộ", "cccd": "Đã mất"},
])

thanh_vien_edited = st.data_editor(df_default, num_rows="dynamic", use_container_width=True)

# --- PHẦN 4: THÔNG TIN NGƯỜI ĐÃ MẤT ---
with st.expander("🕯️ Thông tin thừa kế (Người đã chết)"):
    ca, cb = st.columns(2)
    with ca:
        ten_mat = st.text_input("Họ tên người mất", value="Hán Đức Bình")
        ngay_mat = st.text_input("Ngày mất", value="26/12/2004")
    with cb:
        so_trich_luc = st.text_input("Số Trích lục khai tử", value="470/2025/TLKT-BS")
        ngay_trich_luc = st.text_input("Ngày cấp trích lục", value="22/09/2025")

# --- XỬ LÝ XUẤT FILE ---
def render_docx(tpl_path, context):
    try:
        doc = DocxTemplate(tpl_path)
        doc.render(context)
        out = io.BytesIO()
        doc.save(out)
        return out.getvalue()
    except:
        return None

context = {
    "ho_ten_khai": ho_ten_khai, "nam_sinh_khai": nam_sinh_khai, "cccd_khai": cccd_khai,
    "ngay_cap_khai": ngay_cap_khai, "dia_chi_khai": dia_chi_khai, "so_gcn": so_gcn,
    "thanh_vien": thanh_vien_edited.to_dict('records'),
    "ten_mat": ten_mat, "ngay_mat": ngay_mat, "so_trich_luc": so_trich_luc, "ngay_trich_luc": ngay_trich_luc
}

st.divider()
if st.button("🛠️ TẠO HỒ SƠ WORD"):
    file1 = render_docx("template_cam_ket.docx", context)
    file2 = render_docx("template_to_khai.docx", context)
    
    col_dl1, col_dl2 = st.columns(2)
    if file1:
        col_dl1.download_button("📥 Tải Bản Cam Kết", data=file1, file_name=f"Cam_ket_{ho_ten_khai}.docx")
    if file2:
        col_dl2.download_button("📥 Tải Tờ Khai Thừa Kế", data=file2, file_name=f"To_khai_{ten_mat}.docx")