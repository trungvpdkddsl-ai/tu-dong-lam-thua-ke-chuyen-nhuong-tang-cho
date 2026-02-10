import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
import io
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Phần mềm Hồ sơ Đất đai", layout="wide", page_icon="⚖️")

# --- PHẦN 1: QUẢN LÝ ĐĂNG NHẬP (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.title("🔐 Đăng nhập hệ thống")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Tài khoản")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập", use_container_width=True):
            # Bạn có thể đổi tài khoản/mật khẩu ở đây
            if username == "admin" and password == "123456":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Sai tài khoản hoặc mật khẩu!")

def logout():
    st.session_state['logged_in'] = False
    st.rerun()

# --- PHẦN 2: CÁC FORM CHỨC NĂNG ---

# Hàm hỗ trợ xuất file Word
def generate_doc(template_path, context):
    try:
        doc = DocxTemplate(template_path)
        doc.render(context)
        bio = io.BytesIO()
        doc.save(bio)
        return bio.getvalue()
    except Exception as e:
        st.error(f"Lỗi không tìm thấy file mẫu: {template_path}. Hãy kiểm tra lại Github.")
        return None

def form_thua_ke():
    st.header("📜 Thủ tục: Khai nhận di sản thừa kế")
    
    with st.expander("1. Thông tin người để lại di sản (Người mất)", expanded=True):
        c1, c2 = st.columns(2)
        ten_mat = c1.text_input("Họ tên người mất", "Hán Đức Bình")
        ngay_mat = c2.text_input("Ngày mất", "26/12/2004")
        trich_luc = c1.text_input("Số trích lục khai tử", "470/2025/TLKT-BS")
        
    with st.expander("2. Thông tin người khai (Đại diện)", expanded=True):
        c3, c4 = st.columns(2)
        nguoi_khai = c3.text_input("Họ tên người khai", "Hán Nghị Quyết")
        cccd_khai = c4.text_input("Số CCCD", "025035000185")
        dia_chi_khai = st.text_input("Địa chỉ", "Khu 6, xã Dân Chủ, tỉnh Phú Thọ")

    st.subheader("3. Danh sách hàng thừa kế (Vợ/Chồng/Cha/Mẹ/Con)")
    st.info("💡 Hướng dẫn: Nhấn vào ô để sửa. Nhấn nút dấu (+) dưới cùng để thêm người. Chọn đầu dòng và nhấn Delete để xóa.")
    
    # Tạo bảng dữ liệu mẫu để nhập
    df_mau = pd.DataFrame(columns=["Họ và tên", "Năm sinh", "Quan hệ với người mất", "Số CCCD/Ghi chú"])
    # Thêm 1 dòng ví dụ
    df_mau.loc[0] = ["Nguyễn Thị Đạo", "1934", "Mẹ đẻ", "025134002289"]
    
    # Hiển thị bảng soạn thảo (num_rows="dynamic" cho phép thêm bớt dòng)
    edited_df = st.data_editor(df_mau, num_rows="dynamic", use_container_width=True, key="editor_thua_ke")

    if st.button("Tạo hồ sơ Thừa kế"):
        context = {
            "ten_mat": ten_mat, "ngay_mat": ngay_mat, "trich_luc": trich_luc,
            "nguoi_khai": nguoi_khai, "cccd_khai": cccd_khai, "dia_chi_khai": dia_chi_khai,
            "danh_sach_thua_ke": edited_df.to_dict('records')
        }
        # Tên file mẫu phải khớp với file bạn up lên Github
        file_data = generate_doc("template_thua_ke.docx", context)
        if file_data:
            st.download_button("⬇️ Tải về máy", file_data, f"Ho_so_thua_ke_{ten_mat}.docx")

def form_chuyen_nhuong():
    st.header("🤝 Thủ tục: Chuyển nhượng QSDĐ (Mua bán)")
    
    col_ben_a, col_ben_b = st.columns(2)
    with col_ben_a:
        st.subheader("Bên A (Bên Bán)")
        ten_a = st.text_input("Họ tên chồng (Bên A)")
        cccd_a = st.text_input("CCCD chồng")
        ten_vo_a = st.text_input("Họ tên vợ (Bên A)")
        cccd_vo_a = st.text_input("CCCD vợ")
    
    with col_ben_b:
        st.subheader("Bên B (Bên Mua)")
        ten_b = st.text_input("Họ tên Bên B")
        cccd_b = st.text_input("CCCD Bên B")
        dia_chi_b = st.text_input("Địa chỉ Bên B")

    st.subheader("Thông tin thửa đất")
    thua_dat = st.text_input("Thửa đất số")
    to_ban_do = st.text_input("Tờ bản đồ số")
    dien_tich = st.text_input("Diện tích (m2)")
    gia_ban = st.text_input("Giá chuyển nhượng (VNĐ)")

    if st.button("Tạo hợp đồng Chuyển nhượng"):
        context = {
            "ten_a": ten_a, "cccd_a": cccd_a, "ten_vo_a": ten_vo_a, "cccd_vo_a": cccd_vo_a,
            "ten_b": ten_b, "cccd_b": cccd_b, "dia_chi_b": dia_chi_b,
            "thua_dat": thua_dat, "to_ban_do": to_ban_do, "dien_tich": dien_tich, "gia_ban": gia_ban
        }
        file_data = generate_doc("template_chuyen_nhuong.docx", context)
        if file_data:
            st.download_button("⬇️ Tải Hợp đồng", file_data, f"Hop_dong_CN_{ten_a}.docx")

def form_tang_cho():
    st.header("🎁 Thủ tục: Tặng cho QSDĐ")
    st.write("Nhập thông tin bên Tặng cho và bên Nhận tặng cho...")
    # (Bạn có thể copy logic từ phần Chuyển nhượng sang và đổi tên biến nếu cần)
    st.warning("Đang phát triển form này...")

# --- PHẦN 3: ĐIỀU HƯỚNG CHÍNH (MAIN APP) ---

if not st.session_state['logged_in']:
    login()
else:
    # Sidebar menu
    with st.sidebar:
        st.title("📂 MENU CHỨC NĂNG")
        choice = st.radio("Chọn thủ tục:", ["Thừa kế", "Chuyển nhượng", "Tặng cho"])
        st.divider()
        if st.button("Đăng xuất"):
            logout()
    
    # Hiển thị form tương ứng với lựa chọn
    if choice == "Thừa kế":
        form_thua_ke()
    elif choice == "Chuyển nhượng":
        form_chuyen_nhuong()
    elif choice == "Tặng cho":
        form_tang_cho()
