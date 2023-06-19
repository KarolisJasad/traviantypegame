def calculate_total_generation_rate(village):
    total_generation_rate = {
        'Woodcutter': 0,
        'Clay_pit': 0,
        'Iron_mine': 0,
        'Crop': 0
    }

    village_buildings = village.village_buildings.all()

    for village_building in village_buildings:
        building_name = village_building.building.name
        building_level = village_building.level
        resource_generation_rate = village_building.building.resource_generation_rate.get(str(building_level), 0)

        if building_name == 'Woodcutter':
            total_generation_rate['Woodcutter'] += resource_generation_rate
        elif building_name == 'Clay_pit':
            total_generation_rate['Clay_pit'] += resource_generation_rate
        elif building_name == 'Iron_mine':
            total_generation_rate['Iron_mine'] += resource_generation_rate
        elif building_name == 'Crop':
            total_generation_rate['Crop'] += resource_generation_rate

    return total_generation_rate
