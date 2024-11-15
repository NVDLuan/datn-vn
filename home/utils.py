import random
import string
from django.contrib.auth.models import Group, User, Permission
from home.models import (
    DonVi, ThoiHanLuuTru, LoaiVanBan, PhanLoaiTaiLieuLuuTru,
    KhoLuuTru, GiaLuuTru, PhongLuuTru, MucLucHoSo, HoSo,
    VanBan, TapTinDinhKem, UserDonVi, HopLuuTru
)
from django.apps import apps  # Import apps

# Tạo nhóm quyền với quyền ngẫu nhiên cho các model
def create_groups(group_names=['Admin', 'Editor', 'Viewer']):
    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:  # Chỉ gán quyền nếu nhóm mới được tạo
            # Lấy danh sách tất cả các models (trừ User và Group)
            models = [
                model for model in apps.get_models() 
                if model._meta.app_label == 'home' and model not in [User, Group]
            ]
            # Duyệt qua các model
            for model in models:
                # Lấy danh sách các quyền cho model
                permissions = Permission.objects.filter(content_type__model=model._meta.model_name)
                # Chọn ngẫu nhiên các quyền (list, view, add, change, delete)
                random_permissions = random.sample(list(permissions), random.randint(1, len(permissions)))
                # Gán quyền cho nhóm
                group.permissions.add(*random_permissions)

# Tạo người dùng với staff=True
def create_users(num_users=10):
    for i in range(num_users):
        username = f'user{i+1}'
        password = 'password123'
        email = f'{username}@example.com'
        user = User.objects.create_user(username, email, password)
        user.is_staff = True  # Đặt staff=True
        user.save()

        # Gán nhóm quyền ngẫu nhiên cho người dùng
        groups = Group.objects.order_by('?')[:random.randint(1, 3)]
        user.groups.set(groups)

# Tạo dữ liệu mẫu cho DonVi
def create_donvi_data(num_donvi=10):
    for i in range(num_donvi):
        ten_don_vi = f'Đơn vị {i}'
        ma = f'DV{i+1:03}'
        while DonVi.objects.filter(ma=ma).exists():
            ma = f'DV{random.randint(1, 999):03}'
        donvi = DonVi.objects.create(
            ten_don_vi=ten_don_vi,
            ma=ma,
            mo_ta=f'Mô tả đơn vị {i+1}'
        )
        # Gán nhóm quyền ngẫu nhiên
        groups = Group.objects.order_by('?')[:random.randint(1, 3)]
        donvi.groups.set(groups)

# Tạo dữ liệu mẫu cho UserDonVi
def create_userdonvi_data(num_userdonvi=10):
    users = User.objects.all()
    donvis = DonVi.objects.all()
    for i in range(num_userdonvi):
        user = random.choice(users)
        donvi = random.choice(donvis)
        # Kiểm tra xem cặp user-donvi đã tồn tại chưa
        while UserDonVi.objects.filter(user=user, don_vi=donvi).exists():
            user = random.choice(users)
            donvi = random.choice(donvis)
        UserDonVi.objects.create(
            user=user,
            don_vi=donvi,
            is_admin=random.choice([True, False])
        )

# Tạo dữ liệu mẫu cho ThoiHanLuuTru
def create_thoihanluutru_data(num_thoihan=10):
    for i in range(num_thoihan):
        ten = f'Thời hạn {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        while ThoiHanLuuTru.objects.filter(ten=ten).exists():
            ten = f'Thời hạn {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        ThoiHanLuuTru.objects.create(
            ten=ten,
            so_nam=random.randint(5, 20)
        )

# Tạo dữ liệu mẫu cho LoaiVanBan
def create_loaivanban_data(num_loaivanban=20):
    for i in range(num_loaivanban):
        ten = f'Loại văn bản {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        while LoaiVanBan.objects.filter(ten=ten).exists():
            ten = f'Loại văn bản {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        ten_viet_tat = f'LVB{"".join(random.choices(string.ascii_uppercase, k=3))}'
        while LoaiVanBan.objects.filter(ten_viet_tat=ten_viet_tat).exists():
            ten_viet_tat = f'LVB{"".join(random.choices(string.ascii_uppercase, k=3))}'
        LoaiVanBan.objects.create(
            ten=ten,
            ten_viet_tat=ten_viet_tat
        )

# Tạo dữ liệu mẫu cho PhanLoaiTaiLieuLuuTru
def create_phanloaitailieu_data(num_phanloai=20):
    for i in range(num_phanloai):
        ten = f'Phân loại tài liệu {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        while PhanLoaiTaiLieuLuuTru.objects.filter(ten=ten).exists():
            ten = f'Phân loại tài liệu {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        PhanLoaiTaiLieuLuuTru.objects.create(
            ten=ten,
            mo_ta=f'Mô tả phân loại tài liệu {i+1}'
        )

# Tạo dữ liệu mẫu cho KhoLuuTru
def create_kholuutru_data(num_kho=20):
    for i in range(num_kho):
        ten_kho = f'Kho lưu trữ {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        while KhoLuuTru.objects.filter(ten_kho=ten_kho).exists():
            ten_kho = f'Kho lưu trữ {"".join(random.choices(string.ascii_uppercase + string.digits, k=5))}'
        KhoLuuTru.objects.create(
            ten_kho=ten_kho,
            mo_ta=f'Mô tả kho lưu trữ {i+1}'
        )

# Tạo dữ liệu mẫu cho GiaLuuTru
def create_gialuutru_data(num_gia=20):
    khos = KhoLuuTru.objects.all()
    for i in range(num_gia):
        gia_so = f'Giá số {i+1}'
        while GiaLuuTru.objects.filter(kho_luu_tru=random.choice(khos), gia_so=gia_so).exists():
            gia_so = f'Giá số {random.randint(1, 999):03}'
        GiaLuuTru.objects.create(
            kho_luu_tru=random.choice(khos),
            gia_so=gia_so,
            ten=f'Tên giá {i+1}',
            mo_ta=f'Mô tả giá {i+1}'
        )

# Tạo dữ liệu mẫu cho PhongLuuTru
def create_phongluutru_data(num_phong=150):
    donvis = DonVi.objects.all()
    khos = KhoLuuTru.objects.all()
    for i in range(num_phong):
        phong_so = i + 1
        while PhongLuuTru.objects.filter(phong_so=phong_so).exists():
            phong_so = random.randint(1, 999)
        PhongLuuTru.objects.create(
            name=f'Phòng lưu trữ {i+1}',
            don_vi=random.choice(donvis),
            kho_luu_tru=random.choice(khos),
            phong_so=phong_so,
            lich_su_don_vi_hinh_thanh_phong=f'Lịch sử đơn vị hình thành phòng {i+1}',
            nam_bat_dau=random.randint(1990, 2020),
            nam_ket_thuc=random.randint(2021, 2023)
        )

# Tạo dữ liệu mẫu cho MucLucHoSo
def create_mucluchoso_data(num_mucluc=20):
    phongs = PhongLuuTru.objects.all()
    for i in range(num_mucluc):
        muc_luc_so = f'Mục lục số {i+1}'
        while MucLucHoSo.objects.filter(muc_luc_so=muc_luc_so).exists():
            muc_luc_so = f'Mục lục số {random.randint(1, 999):03}'
        MucLucHoSo.objects.create(
            phong_luu_tru=random.choice(phongs),
            muc_luc_so=muc_luc_so,
            so_trang=random.randint(10, 100)
        )

# Tạo dữ liệu mẫu cho HopLuuTru
def create_hopluutru_data(num_hop=300):
    khos = KhoLuuTru.objects.all()
    gias = GiaLuuTru.objects.all()
    phongs = PhongLuuTru.objects.all()
    muc_lucs = MucLucHoSo.objects.all()
    for i in range(num_hop):
        hop_so = f'Hộp số {i+1}'
        while HopLuuTru.objects.filter(hop_so=hop_so).exists():
            hop_so = f'Hộp số {random.randint(1, 999):03}'
        HopLuuTru.objects.create(
            kho_luu_tru=random.choice(khos),
            gia_luu_tru=random.choice(gias),
            phong_luu_tru=random.choice(phongs),
            muc_luc_ho_so=random.choice(muc_lucs),
            hop_so=hop_so,
            mo_ta=f'Mô tả hộp {i+1}',
            tu_nam=random.randint(2010, 2020),
            den_nam=random.randint(2021, 2023)
        )

# Tạo dữ liệu mẫu cho HoSo
def create_hoso_data(num_hoso=500):
    phongs = PhongLuuTru.objects.all()
    hops = HopLuuTru.objects.all()
    muc_lucs = MucLucHoSo.objects.all()
    phan_loais = PhanLoaiTaiLieuLuuTru.objects.all()
    thoi_hans = ThoiHanLuuTru.objects.all()
    for i in range(num_hoso):
        ho_so_so = f'HS{i+1:04}'
        while HoSo.objects.filter(ho_so_so=ho_so_so).exists():
            ho_so_so = f'HS{random.randint(1, 9999):04}'
        HoSo.objects.create(
            tieu_de=f'Tiêu đề hồ sơ {i+1}',
            ho_so_so=ho_so_so,
            phong_luu_tru=random.choice(phongs),
            hop_luu_tru=random.choice(hops),
            muc_luc_ho_so=random.choice(muc_lucs),
            ma_ho_so=f'MH{i+1:04}',
            phan_loai_tai_lieu_luu_tru=random.choice(phan_loais),
            thoi_han_bao_quan=random.choice(thoi_hans),
            che_do_su_dung='Công khai',
            ngon_ngu='Tiếng Việt',
            tong_so_van_ban_trong_ho_so=random.randint(1, 10),
            thoi_gian_bat_dau=f'{random.randint(2010, 2022)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
            thoi_gian_ket_thuc=f'{random.randint(2010, 2022)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
            so_luong_to=random.randint(1, 5),
            so_luong_trang=random.randint(10, 50)
        )

# Tạo dữ liệu mẫu cho VanBan
def create_vanban_data(num_vanban=100):
    hosos = HoSo.objects.all()
    loai_van_bans = LoaiVanBan.objects.all()
    thoi_hans = ThoiHanLuuTru.objects.all()
    for i in range(num_vanban):
        so_van_ban = f'SVB{i+1:04}'
        while VanBan.objects.filter(so_van_ban=so_van_ban).exists():
            so_van_ban = f'SVB{random.randint(1, 9999):04}'
        VanBan.objects.create(
            ho_so=random.choice(hosos),
            so_thu_tu_van_ban_trong_ho_so=i+1,
            loai_van_ban=random.choice(loai_van_bans),
            ma_dinh_danh_van_ban=f'VB{i+1:04}',
            so_van_ban=so_van_ban,
            ky_hieu_cua_van_ban=f'KHVB{i+1:04}',
            ngay_ban_hanh=f'{random.randint(2010, 2022)}-{random.randint(1, 12)}-{random.randint(1, 28)}',
            co_quan_to_chuc_ban_hanh=f'Cơ quan {i+1}',
            thoi_han_bao_quan=random.choice(thoi_hans),
            trich_yeu_noi_dung=f'Trích yếu nội dung văn bản {i+1}',
            so_luong_trang=random.randint(1, 10)
        )

# ... (Hàm tạo dữ liệu cho TapTinDinhKem - bạn cần tự xử lý phần file đính kèm)

# Gọi các hàm để tạo dữ liệu mẫu
create_groups()
create_users()
create_donvi_data()
create_userdonvi_data()
create_thoihanluutru_data()
create_loaivanban_data()
create_phanloaitailieu_data()
create_kholuutru_data()
create_gialuutru_data()
create_phongluutru_data()
create_mucluchoso_data()
create_hopluutru_data()
create_hoso_data()
create_vanban_data()

print("Đã tạo dữ liệu mẫu!")