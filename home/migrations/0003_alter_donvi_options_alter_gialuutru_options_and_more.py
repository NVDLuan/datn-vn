# Generated by Django 4.2.9 on 2024-11-11 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_vanban_trang_thai'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donvi',
            options={'verbose_name_plural': '00. Đơn Vị'},
        ),
        migrations.AlterModelOptions(
            name='gialuutru',
            options={'verbose_name_plural': '05. Giá Lưu Trữ'},
        ),
        migrations.AlterModelOptions(
            name='hopluutru',
            options={'verbose_name_plural': '07. Hộp Lưu Trữ'},
        ),
        migrations.AlterModelOptions(
            name='kholuutru',
            options={'verbose_name_plural': '04. Kho Lưu Trữ'},
        ),
        migrations.AlterModelOptions(
            name='loaivanban',
            options={'verbose_name_plural': '09. Loại Văn Bản'},
        ),
        migrations.AlterModelOptions(
            name='mucluchoso',
            options={'verbose_name_plural': '06. Mục Lục Hồ Sơ'},
        ),
        migrations.AlterModelOptions(
            name='phanloaitailieuluutru',
            options={'verbose_name_plural': '10. Phân Loại Tài Liệu Lưu Trữ'},
        ),
        migrations.AlterModelOptions(
            name='taptindinhkem',
            options={'verbose_name_plural': '11. Tệp đính kèm'},
        ),
        migrations.AlterModelOptions(
            name='thoihanluutru',
            options={'verbose_name_plural': '08. Thời Hạn Lưu Trữ'},
        ),
        migrations.AlterField(
            model_name='hoso',
            name='ghi_chu',
            field=models.TextField(blank=True, null=True, verbose_name='Ghi chú'),
        ),
        migrations.AlterField(
            model_name='hoso',
            name='phong_luu_tru',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.phongluutru', verbose_name='Phông lưu trữ'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='but_tich',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bút tích'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='ghi_chu',
            field=models.TextField(blank=True, null=True, verbose_name='Ghi chú'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='ky_hieu_thong_tin',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ký hiệu thông tin'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='ma_dinh_danh_van_ban',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Mã định danh văn bản'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='ngon_ngu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ngôn ngữ'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='so_luong_trang',
            field=models.IntegerField(blank=True, null=True, verbose_name='Số lượng trang'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='tinh_trang_vat_ly',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Tình trạng vật lý'),
        ),
        migrations.AlterField(
            model_name='vanban',
            name='tu_khoa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Từ khóa'),
        ),
    ]