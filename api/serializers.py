from rest_framework import serializers
from home.models import (
    DonVi, UserDonVi, KhoLuuTru, GiaLuuTru, PhongLuuTru, MucLucHoSo, HopLuuTru,
    ThoiHanLuuTru, LoaiVanBan, PhanLoaiTaiLieuLuuTru, HoSo, VanBan, TapTinDinhKem
)
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class DonViSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = DonVi
        fields = '__all__'

class UserDonViSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    don_vi = DonViSerializer()

    class Meta:
        model = UserDonVi
        fields = '__all__'

class KhoLuuTruSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhoLuuTru
        fields = '__all__'

class GiaLuuTruSerializer(serializers.ModelSerializer):
    kho_luu_tru = KhoLuuTruSerializer()
    class Meta:
        model = GiaLuuTru
        fields = '__all__'

class PhongLuuTruSerializer(serializers.ModelSerializer):
    don_vi = DonViSerializer()
    kho_luu_tru = KhoLuuTruSerializer()
    class Meta:
        model = PhongLuuTru
        fields = '__all__'

class MucLucHoSoSerializer(serializers.ModelSerializer):
    phong_luu_tru = PhongLuuTruSerializer()
    class Meta:
        model = MucLucHoSo
        fields = '__all__'

class HopLuuTruSerializer(serializers.ModelSerializer):
    kho_luu_tru = KhoLuuTruSerializer()
    gia_luu_tru = GiaLuuTruSerializer()
    phong_luu_tru = PhongLuuTruSerializer()
    muc_luc_ho_so = MucLucHoSoSerializer()
    class Meta:
        model = HopLuuTru
        fields = '__all__'

class ThoiHanLuuTruSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThoiHanLuuTru
        fields = '__all__'

class LoaiVanBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiVanBan
        fields = '__all__'

class PhanLoaiTaiLieuLuuTruSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhanLoaiTaiLieuLuuTru
        fields = '__all__'

class HoSoSerializer(serializers.ModelSerializer):
    phong_luu_tru = PhongLuuTruSerializer()
    hop_luu_tru = HopLuuTruSerializer()
    phan_loai_tai_lieu_luu_tru = PhanLoaiTaiLieuLuuTruSerializer()
    thoi_han_bao_quan = ThoiHanLuuTruSerializer()
    class Meta:
        model = HoSo
        fields = '__all__'

class TapTinDinhKemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TapTinDinhKem
        fields = '__all__'

class VanBanSerializer(serializers.ModelSerializer):
    ho_so = HoSoSerializer()
    loai_van_ban = LoaiVanBanSerializer()
    thoi_han_bao_quan = ThoiHanLuuTruSerializer()
    tep_dinh_kem = TapTinDinhKemSerializer(many=True, read_only=True)
    class Meta:
        model = VanBan
        fields = '__all__'