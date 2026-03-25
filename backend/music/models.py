from django.db import models

class MusicWork(models.Model):
    TYPE_CHOICES = (
        ('audio', '音频作品'),
        ('video', '演出视频'),
        ('photo', '演出照片'),
    )
    
    title = models.CharField(max_length=200, verbose_name="作品名称")
    description = models.TextField(blank=True, null=True, verbose_name="作品简介")
    work_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='audio', verbose_name="类型")
    cover_image = models.ImageField(upload_to='music/covers/', blank=True, null=True, verbose_name="封面图片")
    audio_file = models.FileField(upload_to='music/audio/', blank=True, null=True, verbose_name="音频文件")
    video_file = models.FileField(upload_to='music/video/', blank=True, null=True, verbose_name="视频文件(直接上传)")
    video_url = models.URLField(blank=True, null=True, verbose_name="视频链接(如B站)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "音乐作品"
        verbose_name_plural = "音乐作品"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_work_type_display()})"
