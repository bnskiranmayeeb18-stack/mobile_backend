class ServiceImage(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)