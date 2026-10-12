class ServiceImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, id):
        service = get_object_or_404(Service, id=id, provider=request.user)
        file = request.FILES.get('image')
        if not file: return Response({"success":False,"message":"Missing file"}, status=400)
        img = ServiceImage.objects.create(service=service, image=file)
        return Response({"success":True,"data":{"id":img.id,"url":img.image.url}}, status=201)

    def get(self, request, id):
        service = get_object_or_404(Service, id=id)
        images = service.images.all()
        return Response({"success":True,"data":[{"id":i.id,"url":i.image.url} for i in images]})

    def delete(self, request, id, image_id):
        img = get_object_or_404(ServiceImage, id=image_id, service_id=id, service__provider=request.user)
        img.delete()
        return Response({"success":True,"message":"Deleted"})