from .models import Village, Resource, Building, VillageBuilding


def validate_building_constraints(building, village):
    if building.b_type == 'Resource':
        resource_name = building.name
        same_name_resources_count = village.resources.filter(building__name=resource_name).count()
        if same_name_resources_count >= 4:
            return 'You cannot have more than 4 buildings of the same type.'
    return None


def check_and_deduct_resources(selected_building, village, current_level):
    building_costs = selected_building.building_cost.get(str(current_level + 1))
    wood_cost = building_costs.get('Wood', 0)
    clay_cost = building_costs.get('Clay', 0)
    iron_cost = building_costs.get('Iron', 0)
    crop_cost = building_costs.get('Crop', 0)

    if (
        village.wood_amount >= wood_cost and
        village.clay_amount >= clay_cost and
        village.iron_amount >= iron_cost and
        village.crop_amount >= crop_cost
    ):
        # Deduct resources
        village.wood_amount -= wood_cost
        village.clay_amount -= clay_cost
        village.iron_amount -= iron_cost
        village.crop_amount -= crop_cost
        village.save()
        return building_costs

    return False


def calculate_troop_cost(construction_cost, quantity):
    total_cost = {}
    for resource, cost in construction_cost.items():
        total_cost[resource] = {}
        for res_type, res_cost in cost.items():
            total_cost[resource][res_type] = res_cost * quantity
    return total_cost


def deduct_resources(cost, village):
    # Retrieve the cost dictionary for the troop type
    resource_costs = cost.get('1', {})
    village.wood_amount -= resource_costs.get('Wood', 0)
    village.clay_amount -= resource_costs.get('Clay', 0)
    village.iron_amount -= resource_costs.get('Iron', 0)
    village.crop_amount -= resource_costs.get('Crop', 0)
    village.save()


def check_village_resources(total_cost, village):
    for resource, cost in total_cost.items():
        for res_type, res_cost in cost.items():
            if res_type == 'Wood' and village.wood_amount < res_cost:
                return False
            elif res_type == 'Clay' and village.clay_amount < res_cost:
                return False
            elif res_type == 'Iron' and village.iron_amount < res_cost:
                return False
            elif res_type == 'Crop' and village.crop_amount < res_cost:
                return False
    return True


def create_resource(building, village):
    building_level = building.level
    generation_rate = building.resource_generation_rate.get(str(building_level), 0)
    resource = Resource.objects.create(village=village, generation_rate=generation_rate)
    resource.building.add(building)
    return resource


def create_village_infrastructure(village, building, name):
    village_building = VillageBuilding.objects.create(
        village=village,
        building=building,
        name=name
    )
    village_building.save()
    return village_building


def create_village_building(village, building, resource, name):
    VillageBuilding.objects.create(
        village=village, building=building, resource=resource, name=name)


def upgrade_building_level(village_building):
    village_building.level += 1
    village_building.save()
    return village_building.level


def update_resource_generation_rate(village_building):
    building = village_building.building
    building_level = village_building.level
    new_generation_rate = building.resource_generation_rate.get(str(building_level), 0)
    village_building.resource.generation_rate = new_generation_rate
    village_building.resource.save()


def update_population(village):
    village_buildings = village.village_buildings.all()

    total_population = 0
    for village_building in village_buildings:
        building = village_building.building
        building_level = village_building.level
        building_population = building.population.get(str(building_level), 0)
        total_population += building_population

    village.population = total_population
    village.save()


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




