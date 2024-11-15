from django import forms
from .models import PhongLuuTru, VanBan, HoSo

class PhongLuuTruForm(forms.ModelForm):
    class Meta:
        model = PhongLuuTru
        fields = [
            'name', 'kho_luu_tru', 'phong_so',
            'lich_su_don_vi_hinh_thanh_phong', 'nam_bat_dau',
            'nam_ket_thuc', 'tong_so_tai_lieu_giay',
            'so_luong_tai_lieu_giay_da_so_hoa', 
            'so_luong_trang_tai_lieu_da_lap_ban_sao_bao_hiem',
            'cac_nhom_tai_lieu_chu_yeu', 'cac_loai_hinh_tai_lieu_khac',
            'ngon_ngu', 'cong_cu_tra_cuu', 'ghi_chu', 'trang_thai'
        ]
        # Có thể thêm các tùy chỉnh cho form fields ở đây

class VanBanForm(forms.ModelForm):
    class Meta:
        model = VanBan
        fields = [
            'ho_so', 'so_thu_tu_van_ban_trong_ho_so', 'loai_van_ban', 'ma_dinh_danh_van_ban',
            'so_van_ban', 'ky_hieu_cua_van_ban', 'ngay_ban_hanh', 'co_quan_to_chuc_ban_hanh',
            'thoi_han_bao_quan', 'trich_yeu_noi_dung', 'tu_so', 'den_so', 'ngon_ngu',
            'so_luong_trang', 'ky_hieu_thong_tin', 'tu_khoa', 'che_do_su_dung',
            'muc_do_tin_cay', 'but_tich', 'tinh_trang_vat_ly', 'ghi_chu', 'trang_thai'
        ]

class HoSoForm(forms.ModelForm):
    class Meta:
        model = HoSo
        fields = '__all__'  # Hoặc liệt kê cụ thể các trường bạn muốn hiển thị trong form
        # Ví dụ: fields = ['tieu_de', 'ho_so_so', 'phong_luu_tru', ...]

    # Bạn có thể thêm các tùy chỉnh cho form ở đây, ví dụ:
    # - Thêm widget cho một trường cụ thể
    # - Thêm validator cho một trường cụ thể
    # - Thay đổi label cho một trường cụ thể