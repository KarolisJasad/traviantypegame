def calculate_total_generation_rate(village):
    total_generation_rate = {
        'Woodcutter': 0,
        'Clay_pit': 0,
        'Iron_mine': 0,
        'Crop': 0
    }

    village_buildings = village.village_buildings.filter(building__b_type='Resource')
    village_troops = village.village_troops.all()

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

    for village_troop in village_troops:
        troop_consumption = village_troop.troop.crop_consumption
        total_generation_rate['Crop'] -= village_troop.quantity * troop_consumption

    return total_generation_rate


def update_village_resource_capacity(selected_building, village_building):
    extra_attributes = selected_building.extra_attributes

    if extra_attributes:
        level = village_building.level

        if selected_building.name == 'Granary':
            granary_capacity_data = extra_attributes.get('granarycapacity', {})
            granary_capacity = granary_capacity_data.get(str(level))
            if granary_capacity:
                village_building.village.granary_capacity = granary_capacity

        elif selected_building.name == 'Warehouse':
            warehouse_capacity_data = extra_attributes.get('warehousecapacity', {})
            warehouse_capacity = warehouse_capacity_data.get(str(level))
            if warehouse_capacity:
                village_building.village.warehouse_capacity = warehouse_capacity

        village_building.village.save()



