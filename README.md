

# 📂 Hệ thống Quản lý Hồ Sơ Lưu Trữ 🗄️

[Chèn ảnh chụp màn hình giao diện]

## ✨ Giới thiệu

Hệ thống Quản lý Hồ Sơ Lưu Trữ là một ứng dụng web mạnh mẽ được xây dựng trên nền tảng Django, mang đến giải pháp toàn diện cho việc quản lý và lưu trữ hồ sơ, văn bản một cách hiệu quả và an toàn. Ứng dụng này được thiết kế để đáp ứng nhu cầu của các tổ chức, doanh nghiệp, cơ quan nhà nước trong việc tổ chức tài liệu lưu trữ một cách khoa học và tối ưu.

## 🚀 Tính năng

- 🏢 **Quản lý đơn vị:**
    - ➕ Tạo, 🔄 cập nhật, ❌ xóa thông tin đơn vị (tên, mã, mô tả, trạng thái).
    - 🌳 Quản lý cấu trúc cây đơn vị (đơn vị cha - đơn vị con).
    - 🔑 Phân quyền truy cập theo đơn vị cho người dùng.
- 👥 **Quản lý người dùng và phân quyền:**
    - ➕ Tạo tài khoản người dùng, gán vai trò (👮 Admin, 📝 Editor, 👀 Viewer).
    - 🔑 Gán quyền truy cập chi tiết (xem, thêm, sửa, xóa) cho từng model theo nhóm quyền.
- 📦 **Quản lý kho lưu trữ:**
    - 📦 Quản lý kho lưu trữ, 🗄️ giá lưu trữ, 🚪 phòng lưu trữ.
    - 📊 Theo dõi thông tin chi tiết về vị trí, sức chứa, trạng thái của kho, giá, phòng.
- 📄 **Quản lý hồ sơ:**
    - ➕ Tạo, 🔄 cập nhật, ❌ xóa hồ sơ (tiêu đề, số hồ sơ, phông, hộp, mục lục, mã, loại tài liệu, thời hạn bảo quản,...).
    - 🔄 Quản lý trạng thái hồ sơ (đã số hóa, chưa số hóa).
    - 🔍 Theo dõi thông tin chi tiết về nội dung, thời gian, tình trạng vật lý của hồ sơ.
- 📝 **Quản lý văn bản:**
    - ➕ Thêm, 🔄 sửa, ❌ xóa văn bản trong hồ sơ (loại, số, ngày ban hành, cơ quan ban hành, trích yếu, số trang,...).
    - 📎 Tải lên và quản lý tệp đính kèm cho văn bản.
- 🔍 **Tìm kiếm và lọc nâng cao:**
    - 🔎 Tìm kiếm theo nhiều trường dữ liệu.
    - 🎚️ Lọc theo khoảng thời gian, trạng thái, đơn vị, kho lưu trữ, loại tài liệu,...
- 🖨️ **In ấn hồ sơ:**
    - 📄 Tạo file `.docx` từ template cho từng model.
    - ⚙️ Tùy chỉnh template để in ấn hồ sơ theo định dạng mong muốn.
- 🔄 **Nhập/xuất dữ liệu:**
    - 📥/📤 Nhập/xuất dữ liệu hồ sơ, văn bản dưới dạng file `.csv`.
    - 🔗 Hỗ trợ import/export cho các trường `ForeignKey` và `ManyToManyField`.

## 💻 Công nghệ sử dụng

- **Backend:**
    - 🐍 Django
    - 🌐 Django REST framework
    - 🔑 JWT (JSON Web Token)
    - 💾 SQLite (có thể thay đổi sang PostgreSQL hoặc MySQL)
    - 워드 python-docx
    - 🔄 django-import-export
    - 🔍 django-rangefilter
- **Frontend:**
    - [Chèn các framework/thư viện frontend đã sử dụng (ví dụ: React, Vue.js, Bootstrap)]

## ⚙️ Cài đặt

1. **Clone repository:**

   ```bash
   git clone https://github.com/anhtudotinfo/records-management-mini.git
   ```

2. **Tạo môi trường ảo Python và kích hoạt nó:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Cài đặt các thư viện cần thiết:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình database:**

   - Mở file `settings.py` và cấu hình database (ví dụ: SQLite, PostgreSQL, MySQL).

5. **Chạy migrate database:**

   ```bash
   python manage.py migrate
   ```

6. **Tạo superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Khởi động server:**

   ```bash
   python manage.py runserver
   ```

## 🛠️ Tạo dữ liệu test (Chỉ trong môi trường development)

1. **Mở Django shell:**

   ```bash
   python manage.py shell < home/utils.py
   ```

2. **Chạy script tạo dữ liệu:** (Đảm bảo bạn đã có sẵn file `home/utils.py` với các hàm tạo dữ liệu)

   ```python
   from home.models import *  # Import các model của bạn
   from home.utils import (
       create_groups, create_users, create_donvi_data,
       create_userdonvi_data, create_thoihanluutru_data,
       create_loaivanban_data, create_phanloaitailieu_data,
       create_kholuutru_data, create_gialuutru_data,
       create_phongluutru_data, create_mucluchoso_data,
       create_hopluutru_data, create_hoso_data, 
       create_vanban_data
   )

   # Tạo dữ liệu cho các model
   create_groups()
   create_users()
   create_donvi_data()
   # ... (gọi các hàm tạo dữ liệu khác)

   print("Đã tạo dữ liệu mẫu!")
   ```

3. **Kiểm tra dữ liệu trong Django Admin:** Truy cập `http://127.0.0.1:8000/admin/` và đăng nhập bằng tài khoản superuser.

## 📖 Hướng dẫn sử dụng

[Chèn hướng dẫn sử dụng chi tiết cho ứng dụng]

## 📬 Thông tin liên lạc

- Tác giả: TU NGUYEN, NGA PHAN
- Email: nguyenanhtu.niit@gmail.com
- Github: https://github.com/anhtudotinfo

## ⚠️ Lưu ý:

- Cài đặt đầy đủ các services trước khi chạy

