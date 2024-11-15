from django.urls import path, re_path

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from .views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('phongluutru/', views.phongluutru, name='phongluutru'),
    path('phongluutru/themmoi/', views.phongluutru_themmoi, name='phongluutru_themmoi'),
    path('phongluutru/<int:id>/', views.phongluutru_chitiet, name='phongluutru_chitiet'),
    path('phongluutru/<int:id>/capnhat/', views.phongluutru_capnhat, name='phongluutru_capnhat'),
    path('phongluutru/<int:id>/xoa/', views.phongluutru_xoa, name='phongluutru_xoa'),
    path('vanban/', views.vanban, name='vanban'),
    path('vanban/themmoi/', views.vanban_themmoi, name='vanban_themmoi'),
    path('vanban/<int:id>/', views.vanban_chitiet, name='vanban_chitiet'),
    path('vanban/<int:id>/capnhat/', views.vanban_capnhat, name='vanban_capnhat'),
    path('vanban/<int:id>/xoa/', views.vanban_xoa, name='vanban_xoa'),
    path('hoso/', views.hoso, name='hoso'),
    path('hoso/themmoi/', views.hoso_themmoi, name='hoso_themmoi'),
    path('hoso/<int:id>/', views.hoso_chitiet, name='hoso_chitiet'),
    path('hoso/<int:id>/capnhat/', views.hoso_capnhat, name='hoso_capnhat'),
    path('hoso/<int:id>/xoa/', views.hoso_xoa, name='hoso_xoa'),
    path('print_docx/<str:app_label>/<str:model_name>/<int:pk>/', views.print_docx_view, name='print_to_docx'),
    path('thong-ke-van-ban/', views.thong_ke_van_ban, name='thong_ke_van_ban'),
    path('thong-ke-van-ban/don-vi/', views.thong_ke_don_vi_ajax, name='thong_ke_don_vi_ajax'),
    path('thong-ke-ho-so-het-han/', views.hoso_hethan_view, name='thong_ke_ho_so_het_han'),
    path('hoso/<int:ho_so_id>/export_excel/', views.export_mucluchoso_excel, name='export_mucluchoso_excel'),
    path('hopluutru/<int:ho_so_id>/export_excel/', views.export_hopluutru_excel, name='export_hopluutru_excel'),
    path('muclucvanban/<int:hoso_id>/export_excel/', views.export_muclucvanban_excel, name='export_muclucvanban_excel'),
    path('biahoso/<int:hoso_id>/export_excel/', views.export_biahoso_excel, name='export_biahoso_excel'),
    path('bao-cao-thong-ke/', views.export_bao_cao_thong_ke, name='export_bao_cao_thong_ke'),
    path('in-va-thong-ke/', views.in_va_thong_ke, name='in_va_thong_ke'),
    path('lay-danh-sach-lien-quan/', views.lay_danh_sach_lien_quan, name='lay_danh_sach_lien_quan'),
    # # Authentication
    # path('accounts/login/', LoginView.as_view(), name='login'),
    
    path('in-thoi-han-bao-quan/', views.in_thoi_han_bao_quan, name='in_thoi_han_bao_quan'),
    path('in-muc-luc-ho-so/', views.in_muc_luc_ho_so, name='in_muc_luc_ho_so'),
    path('in-muc-luc-van-ban-thuoc-ho-so/', views.in_muc_luc_van_ban_thuoc_ho_so, name='in_muc_luc_van_ban_thuoc_ho_so'),
    path('in-bia-ho-so/', views.in_bia_ho_so, name='in_bia_ho_so'),
    path('in-phieu-muon/', views.in_phieu_muon, name='in_phieu_muon'),
    path('in-bao-cao-thong-ke/', views.in_bao_cao_thong_ke, name='in_bao_cao_thong_ke'),
    path('phongluutru/<int:phong_luu_tru_id>/export_excel/vv', views.export_mucluchoso_excel_vv, name='export_mucluchoso_excel_vv'),
    path('phongluutru/<int:phong_luu_tru_id>/export_excel/cth', views.export_mucluchoso_excel_cth, name='export_mucluchoso_excel_cth'),
    path('phongluutru/<int:phong_luu_tru_id>/export_excel/loaibo', views.export_mucluchoso_excel_loaibo, name='export_mucluchoso_excel_loaibo'),
]
