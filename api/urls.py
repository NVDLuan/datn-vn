from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # ...
    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # DonVi
    path('api/donvi/', views.DonViList.as_view()),
    path('api/donvi/<int:pk>/', views.DonViDetail.as_view()),

    # UserDonVi
    path('api/userdonvi/', views.UserDonViList.as_view()),
    # ... (Các URL cho UserDonVi Detail, Update, Delete nếu cần)

    # KhoLuuTru
    path('api/kholuutru/', views.KhoLuuTruList.as_view()),
    path('api/kholuutru/<int:pk>/', views.KhoLuuTruDetail.as_view()),

    # GiaLuuTru
    path('api/gialuutru/', views.GiaLuuTruList.as_view()),
    path('api/gialuutru/<int:pk>/', views.GiaLuuTruDetail.as_view()),

    # PhongLuuTru
    path('api/phongluutru/', views.PhongLuuTruList.as_view()),
    path('api/phongluutru/<int:pk>/', views.PhongLuuTruDetail.as_view()),

    # MucLucHoSo
    path('api/mucluchoso/', views.MucLucHoSoList.as_view()),
    path('api/mucluchoso/<int:pk>/', views.MucLucHoSoDetail.as_view()),

    # HopLuuTru
    path('api/hopluutru/', views.HopLuuTruList.as_view()),
    path('api/hopluutru/<int:pk>/', views.HopLuuTruDetail.as_view()),

    # ThoiHanLuuTru
    path('api/thoihanluutru/', views.ThoiHanLuuTruList.as_view()),
    path('api/thoihanluutru/<int:pk>/', views.ThoiHanLuuTruDetail.as_view()),

    # LoaiVanBan
    path('api/loaivanban/', views.LoaiVanBanList.as_view()),
    path('api/loaivanban/<int:pk>/', views.LoaiVanBanDetail.as_view()),

    # PhanLoaiTaiLieuLuuTru
    path('api/phanloaitl/', views.PhanLoaiTaiLieuLuuTruList.as_view()),
    path('api/phanloaitl/<int:pk>/', views.PhanLoaiTaiLieuLuuTruDetail.as_view()),

    # HoSo
    path('api/hoso/', views.HoSoList.as_view()),
    path('api/hoso/<int:pk>/', views.HoSoDetail.as_view()),

    # VanBan
    path('api/vanban/', views.VanBanList.as_view()),
    path('api/vanban/<int:pk>/', views.VanBanDetail.as_view()),

    # TapTinDinhKem
    path('api/vanban/<int:vanban_id>/tepdinhkem/', views.TapTinDinhKemList.as_view()),
    # path('api/vanban/<int:vanban_id>/tepdinhkem/<int:pk>/', views.TapTinDinhKemDetail.as_view()),
]