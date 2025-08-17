from django.db import models
from django.utils.text import slugify
from django.db.models.fields.files import FieldFile

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

class Post(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def file_basename(self):
        if self.file and self.file.name:
            return self.file.name.replace('uploads/', '', 1)
        return ''

    def file_size_display(self):
        if self.file and self.file.name and isinstance(self.file, FieldFile):
            try:
                size = self.file.size
                if size >= 1024 * 1024 * 1024:
                    return f"{size / (1024 * 1024 * 1024):.2f} GB"
                elif size >= 1024 * 1024:
                    return f"{size / (1024 * 1024):.2f} MB"
                elif size >= 1024:
                    return f"{size / 1024:.2f} KB"
                else:
                    return f"{size} B"
            except Exception:
                return ''
        return ''

    def delete(self, *args, **kwargs):
        from django.db.models.fields.files import FieldFile
        if self.file and self.file.name and isinstance(self.file, FieldFile):
            try:
                self.file.delete(save=False)
            except Exception as e:
                # 로그를 남기고, 예외는 무시
                import logging
                logging.error(f'파일 삭제 중 오류: {e}')
                pass
        super().delete(*args, **kwargs)
    
    def delete_file(self):
        """파일만 삭제하는 메서드"""
        import os
        import logging
        logger = logging.getLogger(__name__)
        
        if self.file and self.file.name:
            try:
                # Django FileField의 delete 메서드 사용
                self.file.delete(save=False)
                logger.info(f"파일 삭제 성공: {self.file.name}")
                return True
            except Exception as e:
                logger.error(f'Django FileField delete 중 오류: {e}')
                try:
                    # 직접 파일 시스템에서 삭제 시도
                    file_path = self.file.path if hasattr(self.file, 'path') else None
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                        logger.info(f"직접 파일 삭제 성공: {file_path}")
                        return True
                except Exception as e2:
                    logger.error(f'직접 파일 삭제 중 오류: {e2}')
                    return False
        return False
