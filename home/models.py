from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from django.core.cache import cache

class TimeStampedModelMixin(models.Model):
    """
    Abstract Mixin model to add timestamp
    """
    created_at = models.DateTimeField(u"Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField(u"Ngày cập nhật", auto_now=True, db_index=True)

    class Meta:
        abstract = True

class DonVi(TimeStampedModelMixin):
    """
    Model lưu trữ thông tin về đơn vị
    """
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Đơn vị cha")  # Quan hệ cha-con với chính nó
    ten_don_vi = models.CharField(max_length=255, unique=True, verbose_name="Tên đơn vị")
    ma = models.CharField(max_length=50, unique=True, verbose_name="Mã") 
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")
    groups = models.ManyToManyField(Group, verbose_name="Nhóm quyền", blank=True)  # Quan hệ nhiều-nhiều với Group

    class Meta:
        db_table = 'DonVi'
        verbose_name_plural = '00. Đơn Vị'

    def __str__(self):
        return self.ten_don_vi
    
    @classmethod
    def get_cached_don_vi(cls, don_vi_id):
        cache_key = f'don_vi_{don_vi_id}'
        don_vi = cache.get(cache_key)
        if don_vi is None:
            print(f"Lấy DonVi từ database: {don_vi_id}")
            don_vi = cls.objects.get(pk=don_vi_id)
            cache.set(cache_key, don_vi, 60 * 60)  # Cache đơn vị trong 1 giờ
        else:
            print(f"Lấy DonVi từ cache: {don_vi_id}") 
        return don_vi

class UserDonVi(models.Model):
    """
    Model trung gian giữa Django User và DonVi
    """
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name="Người dùng")
    don_vi = models.ForeignKey(DonVi, on_delete=models.CASCADE, verbose_name="Đơn vị")
    is_admin = models.BooleanField(default=False, verbose_name='Là admin?') # Quyền admin cho đơn vị

    class Meta:
        db_table = 'UserDonVi'
        verbose_name_plural = "02. Quyền truy cập đơn vị"
        unique_together = ('user', 'don_vi') # Đảm bảo mỗi user chỉ có 1 quyền trên 1 đơn vị

    def __str__(self):
        return f"{self.user} - {self.don_vi}"
    
class KhoLuuTru(TimeStampedModelMixin):
    ten_kho = models.CharField(max_length=255, unique=True, verbose_name="Tên kho")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    sap_xep = models.PositiveIntegerField(default=0, verbose_name="Sắp xếp")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")

    class Meta:
        db_table = 'KhoLuuTru'
        verbose_name_plural = '04. Kho Lưu Trữ'

    def __str__(self):
        return self.ten_kho
    
    @classmethod
    def get_cached_kho_luu_tru(cls, kho_luu_tru_id):
        cache_key = f'kho_luu_tru_{kho_luu_tru_id}'
        kho_luu_tru = cache.get(cache_key)
        if kho_luu_tru is None:
            print(f"Lấy KhoLuuTru từ database: {kho_luu_tru_id}")
            kho_luu_tru = cls.objects.get(pk=kho_luu_tru_id)
            cache.set(cache_key, kho_luu_tru, 60 * 60)  # Cache kho lưu trữ trong 1 giờ
        else:
            print(f"Lấy KhoLuuTru từ cache: {kho_luu_tru_id}") 
        return kho_luu_tru
    
class GiaLuuTru(TimeStampedModelMixin):
    kho_luu_tru = models.ForeignKey(
        KhoLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Kho lưu trữ"
    )
    gia_so = models.CharField(max_length=50, verbose_name="Giá số")
    ten = models.CharField(max_length=255, verbose_name="Tên giá")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    sap_xep = models.PositiveIntegerField(default=0, verbose_name="Sắp xếp")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")

    class Meta:
        db_table = 'GiaLuuTru'
        verbose_name_plural = '05. Giá Lưu Trữ'

    def __str__(self):
        return f"{self.gia_so} - {self.ten}"

    @classmethod
    def get_cached_gia_luu_tru(cls, gia_luu_tru_id):
        cache_key = f'gia_luu_tru_{gia_luu_tru_id}'
        gia_luu_tru = cache.get(cache_key)
        if gia_luu_tru is None:
            print(f"Lấy GiaLuuTru từ database: {gia_luu_tru_id}")
            gia_luu_tru = cls.objects.get(pk=gia_luu_tru_id)
            cache.set(cache_key, gia_luu_tru, 60 * 60)  # Cache giá lưu trữ trong 1 giờ
        else:
            print(f"Lấy GiaLuuTru từ cache: {gia_luu_tru_id}") 
        return gia_luu_tru

class PhongLuuTru(TimeStampedModelMixin):
    """
    Model cho Phông lưu trữ
    """
    name = models.CharField(max_length=1024, verbose_name="Tên phông lưu trữ")
    don_vi = models.ForeignKey(DonVi, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Đơn vị")
    kho_luu_tru = models.ForeignKey(
        KhoLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Kho lưu trữ"
    )
    phong_so = models.IntegerField(verbose_name="Phông số")
    lich_su_don_vi_hinh_thanh_phong = models.TextField(blank=True, verbose_name="Lịch sử đơn vị hình thành phòng")
    nam_bat_dau = models.IntegerField(verbose_name="Năm bắt đầu")
    nam_ket_thuc = models.IntegerField(blank=True, null=True, verbose_name="Năm kết thúc")
    tong_so_tai_lieu_giay = models.IntegerField(default=0, verbose_name="Tổng số tài liệu giấy")
    so_luong_tai_lieu_giay_da_so_hoa = models.IntegerField(default=0, verbose_name="Số lượng tài liệu giấy đã số hóa")
    so_luong_trang_tai_lieu_da_lap_ban_sao_bao_hiem = models.IntegerField(default=0, verbose_name="Số lượng trang tài liệu đã lập bản sao bảo hiểm")
    cac_nhom_tai_lieu_chu_yeu = models.TextField(blank=True, verbose_name="Các nhóm tài liệu chủ yếu")
    cac_loai_hinh_tai_lieu_khac = models.TextField(blank=True, verbose_name="Các loại hình tài liệu khác")
    ngon_ngu = models.CharField(max_length=255, blank=True, verbose_name="Ngôn ngữ")
    cong_cu_tra_cuu = models.TextField(blank=True, verbose_name="Công cụ tra cứu")
    ghi_chu = models.TextField(blank=True, verbose_name="Ghi chú")

    TRANG_THAI_CHOICES = [
        ('da_so_hoa', 'Đã số hóa'),
        ('chua_so_hoa', 'Chưa số hóa'),
    ]
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='chua_so_hoa', verbose_name="Trạng thái")

    class Meta:
        db_table = 'PhongLuuTru'
        verbose_name_plural = "01. Phông lưu trữ"

    def __str__(self):
        return self.name
    
    @classmethod
    def get_cached_phong_luu_tru(cls, phong_luu_tru_id):
        cache_key = f'phong_luu_tru_{phong_luu_tru_id}'
        phong_luu_tru = cache.get(cache_key)
        if phong_luu_tru is None:
            print(f"Lấy PhongLuuTru từ database: {phong_luu_tru_id}")
            phong_luu_tru = cls.objects.get(pk=phong_luu_tru_id)
            cache.set(cache_key, phong_luu_tru, 60 * 60)  # Cache Phông lưu trữ trong 1 giờ
        else:
            print(f"Lấy PhongLuuTru từ cache: {phong_luu_tru_id}") 
        return phong_luu_tru

class MucLucHoSo(TimeStampedModelMixin):
    phong_luu_tru = models.ForeignKey(
        PhongLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Phông lưu trữ"
    )
    muc_luc_so = models.CharField(max_length=50, verbose_name="Mục lục số")
    so_trang = models.PositiveIntegerField(default=0, verbose_name="Số trang")
    trang_thai = models.CharField(max_length=50, default="Đang cập nhật", verbose_name="Trạng thái")

    class Meta:
        db_table = 'MucLucHoSo'
        verbose_name_plural = '06. Mục Lục Hồ Sơ'

    def __str__(self):
        return self.muc_luc_so 
    
    @classmethod
    def get_cached_muc_luc_ho_so(cls, muc_luc_ho_so_id):
        cache_key = f'muc_luc_ho_so_{muc_luc_ho_so_id}'
        muc_luc_ho_so = cache.get(cache_key)
        if muc_luc_ho_so is None:
            print(f"Lấy MucLucHoSo từ database: {muc_luc_ho_so_id}")
            muc_luc_ho_so = cls.objects.get(pk=muc_luc_ho_so_id)
            cache.set(cache_key, muc_luc_ho_so, 60 * 60)  # Cache mục lục hồ sơ trong 1 giờ
        else:
            print(f"Lấy MucLucHoSo từ cache: {muc_luc_ho_so_id}") 
        return muc_luc_ho_so

class HopLuuTru(TimeStampedModelMixin):
    kho_luu_tru = models.ForeignKey(
        KhoLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Kho lưu trữ"
    )
    gia_luu_tru = models.ForeignKey(
        GiaLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Giá lưu trữ"
    )
    phong_luu_tru = models.ForeignKey(
        PhongLuuTru, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Phông lưu trữ"
    )
    muc_luc_ho_so = models.ForeignKey(
        MucLucHoSo, 
        on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        verbose_name="Mục lục hồ sơ"
    )
    hop_so = models.CharField(max_length=50, verbose_name="Hộp số")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    tu_nam = models.PositiveIntegerField(blank=True, null=True, verbose_name="Từ năm")
    den_nam = models.PositiveIntegerField(blank=True, null=True, verbose_name="Đến năm")
    trang_thai = models.CharField(max_length=50, default="Còn trống", verbose_name="Trạng thái")

    class Meta:
        db_table = 'HopLuuTru'
        verbose_name_plural = '07. Hộp Lưu Trữ'

    def __str__(self):
        return self.hop_so
    
    @classmethod
    def get_cached_hop_luu_tru(cls, hop_luu_tru_id):
        cache_key = f'hop_luu_tru_{hop_luu_tru_id}'
        hop_luu_tru = cache.get(cache_key)
        if hop_luu_tru is None:
            print(f"Lấy HopLuuTru từ database: {hop_luu_tru_id}")
            hop_luu_tru = cls.objects.get(pk=hop_luu_tru_id)
            cache.set(cache_key, hop_luu_tru, 60 * 60)  # Cache hộp lưu trữ trong 1 giờ
        else:
            print(f"Lấy HopLuuTru từ cache: {hop_luu_tru_id}") 
        return hop_luu_tru
    
class ThoiHanLuuTru(TimeStampedModelMixin):
    ten = models.CharField(max_length=255, unique=True, verbose_name="Tên thời hạn")
    so_nam = models.PositiveIntegerField(verbose_name="Số năm")
    sap_xep = models.PositiveIntegerField(default=0, verbose_name="Sắp xếp")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")

    class Meta:
        db_table = 'ThoiHanLuuTru'
        verbose_name_plural = '08. Thời Hạn Lưu Trữ'

    def __str__(self):
        return self.ten
    
    @classmethod
    def get_cached_thoi_han_luu_tru(cls, thoi_han_luu_tru_id):
        cache_key = f'thoi_han_luu_tru_{thoi_han_luu_tru_id}'
        thoi_han_luu_tru = cache.get(cache_key)
        if thoi_han_luu_tru is None:
            print(f"Lấy ThoiHanLuuTru từ database: {thoi_han_luu_tru_id}")
            thoi_han_luu_tru = cls.objects.get(pk=thoi_han_luu_tru_id)
            cache.set(cache_key, thoi_han_luu_tru, 60 * 60)  # Cache thời hạn lưu trữ trong 1 giờ
        else:
            print(f"Lấy ThoiHanLuuTru từ cache: {thoi_han_luu_tru_id}") 
        return thoi_han_luu_tru
    
class LoaiVanBan(TimeStampedModelMixin):
    ten = models.CharField(max_length=255, unique=True, verbose_name="Tên loại văn bản")
    ten_viet_tat = models.CharField(max_length=50, unique=True, verbose_name="Tên viết tắt")
    sap_xep = models.PositiveIntegerField(default=0, verbose_name="Sắp xếp")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")

    class Meta:
        db_table = 'LoaiVanBan'
        verbose_name_plural = '09. Loại Văn Bản'

    def __str__(self):
        return self.ten
    
    @classmethod
    def get_cached_loai_van_ban(cls, loai_van_ban_id):
        cache_key = f'loai_van_ban_{loai_van_ban_id}'
        loai_van_ban = cache.get(cache_key)
        if loai_van_ban is None:
            print(f"Lấy LoaiVanBan từ database: {loai_van_ban_id}")
            loai_van_ban = cls.objects.get(pk=loai_van_ban_id)
            cache.set(cache_key, loai_van_ban, 60 * 60)  # Cache loại văn bản trong 1 giờ
        else:
            print(f"Lấy LoaiVanBan từ cache: {loai_van_ban_id}") 
        return loai_van_ban
    
class PhanLoaiTaiLieuLuuTru(TimeStampedModelMixin):
    ten = models.CharField(max_length=255, unique=True, verbose_name="Tên phân loại")
    mo_ta = models.TextField(blank=True, verbose_name="Mô tả")
    sap_xep = models.PositiveIntegerField(default=0, verbose_name="Sắp xếp")
    trang_thai = models.BooleanField(default=True, verbose_name="Trạng thái")

    class Meta:
        db_table = 'PhanLoaiTaiLieuLuuTru'
        verbose_name_plural = '10. Phân Loại Tài Liệu Lưu Trữ'

    def __str__(self):
        return self.ten

    @classmethod
    def get_cached_phan_loai_tai_lieu_luu_tru(cls, phan_loai_tai_lieu_luu_tru_id):
        cache_key = f'phan_loai_tai_lieu_luu_tru_{phan_loai_tai_lieu_luu_tru_id}'
        phan_loai_tai_lieu_luu_tru = cache.get(cache_key)
        if phan_loai_tai_lieu_luu_tru is None:
            print(f"Lấy PhanLoaiTaiLieuLuuTru từ database: {phan_loai_tai_lieu_luu_tru_id}")
            phan_loai_tai_lieu_luu_tru = cls.objects.get(pk=phan_loai_tai_lieu_luu_tru_id)
            cache.set(cache_key, phan_loai_tai_lieu_luu_tru, 60 * 60)  # Cache phân loại tài liệu lưu trữ trong 1 giờ
        else:
            print(f"Lấy PhanLoaiTaiLieuLuuTru từ cache: {phan_loai_tai_lieu_luu_tru_id}") 
        return phan_loai_tai_lieu_luu_tru
    
class HoSo(TimeStampedModelMixin):
    """
    Model cho Hồ sơ
    """
    tieu_de = models.CharField(max_length=255, verbose_name="Tiêu đề")
    ho_so_so = models.CharField(max_length=50, verbose_name="Hồ sơ số")
    phong_luu_tru = models.ForeignKey(PhongLuuTru, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Phông lưu trữ")
    hop_luu_tru = models.ForeignKey(HopLuuTru, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Hộp lưu trữ")
    muc_luc_ho_so = models.ForeignKey(MucLucHoSo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mục lục hồ sơ")
    ma_ho_so = models.CharField(max_length=50, null=True, blank=True, verbose_name="Mã hồ sơ")
    phan_loai_tai_lieu_luu_tru = models.ForeignKey(PhanLoaiTaiLieuLuuTru, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Loại tài liệu lưu trữ")
    thoi_han_bao_quan = models.ForeignKey(ThoiHanLuuTru, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Thời hạn bảo quản")
    che_do_su_dung = models.CharField(max_length=255, verbose_name="Chế độ sử dụng")
    ngon_ngu = models.CharField(max_length=100, verbose_name="Ngôn ngữ")
    tong_so_van_ban_trong_ho_so = models.IntegerField(default=0, verbose_name="Tổng số văn bản trong hồ sơ")
    thoi_gian_bat_dau = models.DateField(verbose_name="Thời gian bắt đầu")
    thoi_gian_ket_thuc = models.DateField(blank=True, null=True, verbose_name="Thời gian kết thúc")
    chu_giai = models.TextField(blank=True, verbose_name="Chú giải")
    ky_hieu_thong_tin = models.CharField(max_length=100, blank=True, verbose_name="Ký hiệu thông tin")
    tu_khoa = models.CharField(max_length=255, blank=True, verbose_name="Từ khóa")
    so_luong_to = models.IntegerField(default=0, verbose_name="Số lượng tờ")
    so_luong_trang = models.IntegerField(default=0, verbose_name="Số lượng trang")
    tinh_trang_vat_ly = models.TextField(blank=True, verbose_name="Tình trạng vật lý")
    ghi_chu = models.TextField(null=True, blank=True, verbose_name="Ghi chú")

    TRANG_THAI_CHOICES = [
        ('da_so_hoa', 'Đã số hóa'),
        ('chua_so_hoa', 'Chưa số hóa'),
    ]
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='chua_so_hoa', verbose_name="Trạng thái")

    class Meta:
        db_table = 'HoSo'
        verbose_name_plural = '02. Hồ Sơ'

    def __str__(self):
        return f"{self.ho_so_so} - {self.tieu_de}"
    
    @classmethod
    def get_cached_ho_so(cls, ho_so_id):
        cache_key = f'ho_so_{ho_so_id}'
        ho_so = cache.get(cache_key)
        if ho_so is None:
            print(f"Lấy HoSo từ database: {ho_so_id}")
            ho_so = cls.objects.get(pk=ho_so_id)
            cache.set(cache_key, ho_so, 60 * 60)  # Cache hồ sơ trong 1 giờ
        else:
            print(f"Lấy HoSo từ cache: {ho_so_id}") 
        return ho_so

class VanBan(TimeStampedModelMixin):
    """
    Model cho Văn bản
    """
    ho_so = models.ForeignKey(HoSo, on_delete=models.CASCADE, verbose_name="Hồ sơ")
    so_thu_tu_van_ban_trong_ho_so = models.IntegerField(verbose_name="Số thứ tự văn bản trong hồ sơ")
    loai_van_ban = models.ForeignKey(LoaiVanBan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Loại văn bản")
    ma_dinh_danh_van_ban = models.CharField(null=True, blank=True,max_length=50, verbose_name="Mã định danh văn bản")
    so_van_ban = models.CharField(max_length=50, verbose_name="Số văn bản")
    ky_hieu_cua_van_ban = models.CharField(max_length=50, verbose_name="Ký hiệu của văn bản")
    ngay_ban_hanh = models.DateField(verbose_name="Ngày ban hành")
    co_quan_to_chuc_ban_hanh = models.CharField(max_length=255, verbose_name="Cơ quan/Tổ chức ban hành")
    thoi_han_bao_quan = models.ForeignKey(ThoiHanLuuTru, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Thời hạn bảo quản")
    trich_yeu_noi_dung = models.TextField(verbose_name="Trích yếu nội dung")
    tu_so = models.IntegerField(null=True, blank=True, verbose_name="Từ số")
    den_so = models.IntegerField(null=True, blank=True, verbose_name="Đến số")
    ngon_ngu = models.CharField(null=True, blank=True,max_length=100, verbose_name="Ngôn ngữ")
    so_luong_trang = models.IntegerField(null=True, blank=True,verbose_name="Số lượng trang")
    ky_hieu_thong_tin = models.CharField(null=True, blank=True,max_length=100, verbose_name="Ký hiệu thông tin")
    tu_khoa = models.CharField(null=True, blank=True,max_length=255, verbose_name="Từ khóa")
    che_do_su_dung = models.CharField(max_length=100, verbose_name="Chế độ sử dụng")
    muc_do_tin_cay = models.CharField(max_length=100, verbose_name="Mức độ tin cậy")
    but_tich = models.CharField(null=True, blank=True,max_length=255, verbose_name="Bút tích")
    tinh_trang_vat_ly = models.CharField(null=True, blank=True,max_length=255, verbose_name="Tình trạng vật lý")
    ghi_chu = models.TextField(null=True, blank=True,verbose_name="Ghi chú")
    #tap_tin_dinh_kem = models.FileField(upload_to='uploads/', null=True, blank=True, verbose_name="Tệp đính kèm")
    TRANG_THAI_CHOICES = [
        ('da_so_hoa', 'Đã số hóa'),
        ('chua_so_hoa', 'Chưa số hóa'),
    ]
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='chua_so_hoa', verbose_name="Trạng thái")

    def __str__(self):
        return f"{self.so_van_ban} - {self.ky_hieu_cua_van_ban}"

    class Meta:
        db_table = 'VanBan'
        verbose_name_plural = '03. Văn Bản'
    
    @classmethod
    def get_cached_van_ban(cls, van_ban_id):
        cache_key = f'van_ban_{van_ban_id}'
        van_ban = cache.get(cache_key)
        if van_ban is None:
            print(f"Lấy VanBan từ database: {van_ban_id}")
            van_ban = cls.objects.get(pk=van_ban_id)
            cache.set(cache_key, van_ban, 60 * 60)  # Cache văn bản trong 1 giờ
        else:
            print(f"Lấy VanBan từ cache: {van_ban_id}") 
        return van_ban

class TapTinDinhKem(models.Model):
    """
    Model cho Tệp đính kèm
    """
    van_ban = models.ForeignKey(VanBan, on_delete=models.CASCADE, related_name='tep_dinh_kem', verbose_name="Văn bản")
    tep_tin = models.FileField(upload_to='uploads/vanban/%Y/%m/%d/', verbose_name="Tệp tin")

    class Meta:
        db_table = 'TapTinDinhKem'
        verbose_name_plural = '11. Tệp đính kèm'

    def __str__(self):
        
        return f"Tệp đính kèm của {self.van_ban}"