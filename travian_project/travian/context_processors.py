def village_context(request):
    village = None
    if request.user.is_authenticated:
        village = request.user.village.first()
    return {'village': village}