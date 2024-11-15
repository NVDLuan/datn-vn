from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from home.models import (
    DonVi, UserDonVi, KhoLuuTru, GiaLuuTru, PhongLuuTru, MucLucHoSo, HopLuuTru,
    ThoiHanLuuTru, LoaiVanBan, PhanLoaiTaiLieuLuuTru, HoSo, VanBan, TapTinDinhKem
)
from .serializers import (
    DonViSerializer, UserDonViSerializer, KhoLuuTruSerializer, GiaLuuTruSerializer,
    PhongLuuTruSerializer, MucLucHoSoSerializer, HopLuuTruSerializer,
    ThoiHanLuuTruSerializer, LoaiVanBanSerializer, PhanLoaiTaiLieuLuuTruSerializer,
    HoSoSerializer, VanBanSerializer, TapTinDinhKemSerializer
)

class DataPermission(permissions.BasePermission):
    """
    Kiểm tra quyền truy cập dữ liệu dựa trên đơn vị và nhóm
    """

    def has_permission(self, request, view):
        # Cho phép truy cập GET cho tất cả user đã xác thực
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        # Các phương thức khác yêu cầu xác thực và kiểm tra quyền
        return self.check_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return self.check_permission(request, view, obj)

    def check_permission(self, request, view, obj=None):
        # Superuser luôn có quyền truy cập
        if request.user.is_superuser:
            return True

        # Nếu user không thuộc đơn vị nào, không cho phép truy cập
        if request.user.is_authenticated:
            user_donvis = UserDonVi.objects.filter(user=request.user)
            if not user_donvis.exists():
                return False

            # Lấy danh sách ID đơn vị mà user có quyền truy cập
            donvi_ids = user_donvis.values_list('don_vi_id', flat=True)

            # Kiểm tra quyền truy cập dựa trên model
            if isinstance(obj, DonVi):
                return obj.id in donvi_ids
            elif isinstance(obj, PhongLuuTru):
                return obj.don_vi_id in donvi_ids
            elif isinstance(obj, MucLucHoSo):
                return obj.phong_luu_tru.don_vi_id in donvi_ids
            elif isinstance(obj, HopLuuTru):
                return obj.phong_luu_tru.don_vi_id in donvi_ids
            elif isinstance(obj, HoSo):
                return obj.phong_luu_tru.don_vi_id in donvi_ids
            elif isinstance(obj, VanBan):
                return obj.ho_so.phong_luu_tru.don_vi_id in donvi_ids
            elif isinstance(obj, TapTinDinhKem):
                return obj.van_ban.ho_so.phong_luu_tru.don_vi_id in donvi_ids

            # Kiểm tra quyền truy cập dựa trên group (nếu cần)
            user_groups = request.user.groups.all()
            if isinstance(obj, DonVi):
                return any(group in obj.groups.all() for group in user_groups)
            # Tương tự cho các models khác nếu cần kiểm tra group

        return False

# Views cho DonVi
class DonViList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        # Superuser xem tất cả, user khác xem theo quyền
        if request.user.is_superuser:
            don_vis = DonVi.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            don_vis = DonVi.objects.filter(id__in=donvi_ids)
        else:
            don_vis = DonVi.objects.none() # Hoặc xử lý theo logic của bạn cho AnonymousUser
        serializer = DonViSerializer(don_vis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DonViSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonViDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return DonVi.objects.get(pk=pk)
        except DonVi.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        don_vi = self.get_object(pk)
        self.check_object_permissions(request, don_vi)
        serializer = DonViSerializer(don_vi)
        return Response(serializer.data)

    def put(self, request, pk):
        don_vi = self.get_object(pk)
        self.check_object_permissions(request, don_vi)
        serializer = DonViSerializer(don_vi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        don_vi = self.get_object(pk)
        self.check_object_permissions(request, don_vi)
        don_vi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Views cho UserDonVi
class UserDonViList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_don_vis = UserDonVi.objects.filter(user=request.user)
        serializer = UserDonViSerializer(user_don_vis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserDonViSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDonViDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return UserDonVi.objects.get(pk=pk)
        except UserDonVi.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user_don_vi = self.get_object(pk)
        self.check_object_permissions(request, user_don_vi)
        serializer = UserDonViSerializer(user_don_vi)
        return Response(serializer.data)

    def put(self, request, pk):
        user_don_vi = self.get_object(pk)
        self.check_object_permissions(request, user_don_vi)
        serializer = UserDonViSerializer(user_don_vi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_don_vi = self.get_object(pk)
        self.check_object_permissions(request, user_don_vi)
        user_don_vi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class KhoLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            kho_luu_trus = KhoLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            kho_luu_trus = KhoLuuTru.objects.filter(id__in=donvi_ids)
        else:
            kho_luu_trus = KhoLuuTru.objects.none()
        serializer = KhoLuuTruSerializer(kho_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KhoLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KhoLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return KhoLuuTru.objects.get(pk=pk)
        except KhoLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        kho_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, kho_luu_tru)
        serializer = KhoLuuTruSerializer(kho_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        kho_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, kho_luu_tru)
        serializer = KhoLuuTruSerializer(kho_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        kho_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, kho_luu_tru)
        kho_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GiaLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            gia_luu_trus = GiaLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            gia_luu_trus = GiaLuuTru.objects.filter(kho_luu_tru__in=donvi_ids)
        else:
            gia_luu_trus = GiaLuuTru.objects.none()
        serializer = GiaLuuTruSerializer(gia_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GiaLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GiaLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return GiaLuuTru.objects.get(pk=pk)
        except GiaLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        gia_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, gia_luu_tru)
        serializer = GiaLuuTruSerializer(gia_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        gia_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, gia_luu_tru)
        serializer = GiaLuuTruSerializer(gia_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        gia_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, gia_luu_tru)
        gia_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PhongLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            phong_luu_trus = PhongLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            phong_luu_trus = PhongLuuTru.objects.filter(don_vi__in=donvi_ids)
        else:
            phong_luu_trus = PhongLuuTru.objects.none()
        serializer = PhongLuuTruSerializer(phong_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhongLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhongLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return PhongLuuTru.objects.get(pk=pk)
        except PhongLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        phong_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phong_luu_tru)
        serializer = PhongLuuTruSerializer(phong_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        phong_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phong_luu_tru)
        serializer = PhongLuuTruSerializer(phong_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        phong_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phong_luu_tru)
        phong_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MucLucHoSoList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            muc_luc_ho_sos = MucLucHoSo.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            muc_luc_ho_sos = MucLucHoSo.objects.filter(phong_luu_tru__don_vi__in=donvi_ids)
        else:
            muc_luc_ho_sos = MucLucHoSo.objects.none()
        serializer = MucLucHoSoSerializer(muc_luc_ho_sos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MucLucHoSoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MucLucHoSoDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return MucLucHoSo.objects.get(pk=pk)
        except MucLucHoSo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        muc_luc_ho_so = self.get_object(pk)
        self.check_object_permissions(request, muc_luc_ho_so)
        serializer = MucLucHoSoSerializer(muc_luc_ho_so)
        return Response(serializer.data)

    def put(self, request, pk):
        muc_luc_ho_so = self.get_object(pk)
        self.check_object_permissions(request, muc_luc_ho_so)
        serializer = MucLucHoSoSerializer(muc_luc_ho_so, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        muc_luc_ho_so = self.get_object(pk)
        self.check_object_permissions(request, muc_luc_ho_so)
        muc_luc_ho_so.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HopLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            hop_luu_trus = HopLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            hop_luu_trus = HopLuuTru.objects.filter(phong_luu_tru__don_vi__in=donvi_ids)
        else:
            hop_luu_trus = HopLuuTru.objects.none()
        serializer = HopLuuTruSerializer(hop_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HopLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HopLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return HopLuuTru.objects.get(pk=pk)
        except HopLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        hop_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, hop_luu_tru)
        serializer = HopLuuTruSerializer(hop_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        hop_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, hop_luu_tru)
        serializer = HopLuuTruSerializer(hop_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hop_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, hop_luu_tru)
        hop_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ThoiHanLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            thoi_han_luu_trus = ThoiHanLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            thoi_han_luu_trus = ThoiHanLuuTru.objects.filter(id__in=donvi_ids)
        else:
            thoi_han_luu_trus = ThoiHanLuuTru.objects.none()
        serializer = ThoiHanLuuTruSerializer(thoi_han_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThoiHanLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThoiHanLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return ThoiHanLuuTru.objects.get(pk=pk)
        except ThoiHanLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        thoi_han_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, thoi_han_luu_tru)
        serializer = ThoiHanLuuTruSerializer(thoi_han_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        thoi_han_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, thoi_han_luu_tru)
        serializer = ThoiHanLuuTruSerializer(thoi_han_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        thoi_han_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, thoi_han_luu_tru)
        thoi_han_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoaiVanBanList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            loai_van_bans = LoaiVanBan.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            loai_van_bans = LoaiVanBan.objects.filter(id__in=donvi_ids)
        else:
            loai_van_bans = LoaiVanBan.objects.none()
        serializer = LoaiVanBanSerializer(loai_van_bans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LoaiVanBanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoaiVanBanDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return LoaiVanBan.objects.get(pk=pk)
        except LoaiVanBan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        loai_van_ban = self.get_object(pk)
        self.check_object_permissions(request, loai_van_ban)
        serializer = LoaiVanBanSerializer(loai_van_ban)
        return Response(serializer.data)

    def put(self, request, pk):
        loai_van_ban = self.get_object(pk)
        self.check_object_permissions(request, loai_van_ban)
        serializer = LoaiVanBanSerializer(loai_van_ban, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        loai_van_ban = self.get_object(pk)
        self.check_object_permissions(request, loai_van_ban)
        loai_van_ban.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PhanLoaiTaiLieuLuuTruList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            phan_loai_tai_lieu_luu_trus = PhanLoaiTaiLieuLuuTru.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            phan_loai_tai_lieu_luu_trus = PhanLoaiTaiLieuLuuTru.objects.filter(id__in=donvi_ids)
        else:
            phan_loai_tai_lieu_luu_trus = PhanLoaiTaiLieuLuuTru.objects.none()
        serializer = PhanLoaiTaiLieuLuuTruSerializer(phan_loai_tai_lieu_luu_trus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhanLoaiTaiLieuLuuTruSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhanLoaiTaiLieuLuuTruDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return PhanLoaiTaiLieuLuuTru.objects.get(pk=pk)
        except PhanLoaiTaiLieuLuuTru.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        phan_loai_tai_lieu_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phan_loai_tai_lieu_luu_tru)
        serializer = PhanLoaiTaiLieuLuuTruSerializer(phan_loai_tai_lieu_luu_tru)
        return Response(serializer.data)

    def put(self, request, pk):
        phan_loai_tai_lieu_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phan_loai_tai_lieu_luu_tru)
        serializer = PhanLoaiTaiLieuLuuTruSerializer(phan_loai_tai_lieu_luu_tru, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        phan_loai_tai_lieu_luu_tru = self.get_object(pk)
        self.check_object_permissions(request, phan_loai_tai_lieu_luu_tru)
        phan_loai_tai_lieu_luu_tru.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HoSoList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            ho_sos = HoSo.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            ho_sos = HoSo.objects.filter(phong_luu_tru__don_vi__in=donvi_ids)
        else:
            ho_sos = HoSo.objects.none()
        serializer = HoSoSerializer(ho_sos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HoSoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HoSoDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return HoSo.objects.get(pk=pk)
        except HoSo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        ho_so = self.get_object(pk)
        self.check_object_permissions(request, ho_so)
        serializer = HoSoSerializer(ho_so)
        return Response(serializer.data)

    def put(self, request, pk):
        ho_so = self.get_object(pk)
        self.check_object_permissions(request, ho_so)
        serializer = HoSoSerializer(ho_so, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ho_so = self.get_object(pk)
        self.check_object_permissions(request, ho_so)
        ho_so.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VanBanList(APIView):
    permission_classes = [DataPermission]

    def get(self, request):
        if request.user.is_superuser:
            van_bans = VanBan.objects.all()
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            van_bans = VanBan.objects.filter(ho_so__phong_luu_tru__don_vi__in=donvi_ids)
        else:
            van_bans = VanBan.objects.none()
        serializer = VanBanSerializer(van_bans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VanBanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VanBanDetail(APIView):
    permission_classes = [DataPermission]

    def get_object(self, pk):
        try:
            return VanBan.objects.get(pk=pk)
        except VanBan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        van_ban = self.get_object(pk)
        self.check_object_permissions(request, van_ban)
        serializer = VanBanSerializer(van_ban)
        return Response(serializer.data)

    def put(self, request, pk):
        van_ban = self.get_object(pk)
        self.check_object_permissions(request, van_ban)
        serializer = VanBanSerializer(van_ban, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        van_ban = self.get_object(pk)
        self.check_object_permissions(request, van_ban)
        van_ban.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TapTinDinhKemList(APIView):
    permission_classes = [DataPermission]

    def get(self, request, vanban_id):
        if request.user.is_superuser:
            tep_dinh_kems = TapTinDinhKem.objects.filter(van_ban_id=vanban_id)
        elif request.user.is_authenticated:
            donvi_ids = UserDonVi.objects.filter(user=request.user).values_list('don_vi_id', flat=True)
            tep_dinh_kems = TapTinDinhKem.objects.filter(van_ban_id=vanban_id, van_ban__ho_so__phong_luu_tru__don_vi__in=donvi_ids)
        else:
            van_bans = VanBan.objects.none()
        serializer = TapTinDinhKemSerializer(tep_dinh_kems, many=True)
        return Response(serializer.data)

    def post(self, request, vanban_id):
        serializer = TapTinDinhKemSerializer(data=request.data, context={'vanban_id': vanban_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD)