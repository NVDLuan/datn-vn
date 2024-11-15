from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import *
from django.contrib.auth.models import Group
from import_export.widgets import DateWidget
class GroupWidget(ManyToManyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()
        if isinstance(value, str):
            values = value.split(self.separator)
            return self.model.objects.filter(name__in=values)
        elif isinstance(value, (list, tuple)):
            return self.model.objects.filter(name__in=value)
        return self.model.objects.none()

class DonViResource(resources.ModelResource):
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(DonVi, 'ten_don_vi'),
    )
    groups = fields.Field(
        column_name='groups',
        attribute='groups',
        widget=GroupWidget(Group, field='name', separator=', '),
    )
    class Meta:
        model = DonVi
        #fields = ('id', 'parent', 'ten_don_vi', 'ma', 'mo_ta', 'trang_thai')
        #exclude = ('created_at', 'updated_at')  # Loại trừ trường nếu cần

class UserDonViResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(DjangoUser, 'username')
    )
    don_vi = fields.Field(
        column_name='don_vi',
        attribute='don_vi',
        widget=ForeignKeyWidget(DonVi, 'ten_don_vi')
    )
    class Meta:
        model = UserDonVi
        
class KhoLuuTruResource(resources.ModelResource):
    class Meta:
        model = KhoLuuTru

class GiaLuuTruResource(resources.ModelResource):
    kho_luu_tru = fields.Field(
        column_name='kho_luu_tru',
        attribute='kho_luu_tru',
        widget=ForeignKeyWidget(KhoLuuTru, 'ten_kho')
    )
    class Meta:
        model = GiaLuuTru

class PhongLuuTruResource(resources.ModelResource):
    don_vi = fields.Field(
        column_name='don_vi',
        attribute='don_vi',
        widget=ForeignKeyWidget(DonVi, 'ten_don_vi')
    )
    kho_luu_tru = fields.Field(
        column_name='kho_luu_tru',
        attribute='kho_luu_tru',
        widget=ForeignKeyWidget(KhoLuuTru, 'ten_kho')
    )
    class Meta:
        model = PhongLuuTru

class MucLucHoSoResource(resources.ModelResource):
    phong_luu_tru = fields.Field(
        column_name='phong_luu_tru',
        attribute='phong_luu_tru',
        widget=ForeignKeyWidget(PhongLuuTru, 'name')
    )
    class Meta:
        model = MucLucHoSo

class HopLuuTruResource(resources.ModelResource):
    kho_luu_tru = fields.Field(
        column_name='kho_luu_tru',
        attribute='kho_luu_tru',
        widget=ForeignKeyWidget(KhoLuuTru, 'ten_kho')
    )
    gia_luu_tru = fields.Field(
        column_name='gia_luu_tru',
        attribute='gia_luu_tru',
        widget=ForeignKeyWidget(GiaLuuTru, 'ten')
    )
    phong_luu_tru = fields.Field(
        column_name='phong_luu_tru',
        attribute='phong_luu_tru',
        widget=ForeignKeyWidget(PhongLuuTru, 'name')
    )
    muc_luc_ho_so = fields.Field(
        column_name='muc_luc_ho_so',
        attribute='muc_luc_ho_so',
        widget=ForeignKeyWidget(MucLucHoSo, 'muc_luc_so')
    )
    class Meta:
        model = HopLuuTru

class ThoiHanLuuTruResource(resources.ModelResource):
    class Meta:
        model = ThoiHanLuuTru

class LoaiVanBanResource(resources.ModelResource):
    class Meta:
        model = LoaiVanBan

class PhanLoaiTaiLieuLuuTruResource(resources.ModelResource):
    class Meta:
        model = PhanLoaiTaiLieuLuuTru

class HoSoResource(resources.ModelResource):
    phong_luu_tru = fields.Field(
        column_name='phong_luu_tru',
        attribute='phong_luu_tru',
        widget=ForeignKeyWidget(PhongLuuTru, 'name')
    )
    hop_luu_tru = fields.Field(
        column_name='hop_luu_tru',
        attribute='hop_luu_tru',
        widget=ForeignKeyWidget(HopLuuTru, 'hop_so')
    )
    muc_luc_ho_so = fields.Field(
        column_name='muc_luc_ho_so',
        attribute='muc_luc_ho_so',
        widget=ForeignKeyWidget(MucLucHoSo, 'muc_luc_so')
    )
    phan_loai_tai_lieu_luu_tru = fields.Field(
        column_name='phan_loai_tai_lieu_luu_tru',
        attribute='phan_loai_tai_lieu_luu_tru',
        widget=ForeignKeyWidget(PhanLoaiTaiLieuLuuTru, 'ten')
    )
    thoi_han_bao_quan = fields.Field(
        column_name='thoi_han_bao_quan',
        attribute='thoi_han_bao_quan',
        widget=ForeignKeyWidget(ThoiHanLuuTru, 'ten')
    )

    thoi_gian_bat_dau = fields.Field(
        column_name='thoi_gian_bat_dau',
        attribute='thoi_gian_bat_dau',
        widget=DateWidget(format='%d/%m/%Y')  # e.g., format as YYYY-MM-DD
    )

    thoi_gian_ket_thuc = fields.Field(
        column_name='thoi_gian_ket_thuc',
        attribute='thoi_gian_ket_thuc',
        widget=DateWidget(format='%d/%m/%Y')  # e.g., format as YYYY-MM-DD
    )


    class Meta:
        model = HoSo

class VanBanResource(resources.ModelResource):
    ho_so = fields.Field(
        column_name='ho_so',
        attribute='ho_so',
        widget=ForeignKeyWidget(HoSo, 'tieu_de')
    )
    loai_van_ban = fields.Field(
        column_name='loai_van_ban',
        attribute='loai_van_ban',
        widget=ForeignKeyWidget(LoaiVanBan, 'ten')
    )
    thoi_han_bao_quan = fields.Field(
        column_name='thoi_han_bao_quan',
        attribute='thoi_han_bao_quan',
        widget=ForeignKeyWidget(ThoiHanLuuTru, 'ten')
    )

    ngay_ban_hanh = fields.Field(
        column_name='ngay_ban_hanh',
        attribute='ngay_ban_hanh',
        widget=DateWidget(format='%d/%m/%Y')  # e.g., format as YYYY-MM-DD
    )
    class Meta:
        model = VanBan