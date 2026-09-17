from lib.scripts.metro_constants import SHAPES, SHAPE_IDS, TRIPS
total_points = 0
distances = []
for route_id in TRIPS:
    for trip_id in TRIPS[route_id]:
        shape_id = SHAPE_IDS.get((route_id, trip_id), None)

        if not shape_id:
            continue

        shape_points = SHAPES.get(shape_id, None)

        if not shape_points:
            continue

        prev_dist_traveled = 0
        for point in shape_points:
            total_points += 1
            try: 
                dist = float(point[2]) - prev_dist_traveled
            except Exception as e:
                print(f"{e} : point[2]")
                continue
            if dist <= 0:
                continue
            distances.append(dist)
            prev_dist_traveled = float(point[2])

print(sum(distances) / total_points) # average distance traveled

