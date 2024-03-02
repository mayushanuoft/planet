import geojson
import os
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

def load_data() -> str:
    ## Load the GeoJSON ##
    while True:
        input_format = input("Would you like to pass the GeoJSON as a string or file path? (Please enter either 'string' or 'file' exactly as shown): ")
        if input_format == 'string':
            input_geojson = input("Please enter a single GeoJSON string: ")
            break
        elif input_format == 'file':
            input_geojson = input("Please enter the file path: ")
            if not os.path.exists(input_geojson):
                print("The file path does not exist. Please enter a valid file path.")
                continue
            break
        else:
            print("Invalid input. Please enter either 'string' or 'file' exactly as shown: ")

    return input_geojson

def validate_input(input_geojson: str):
    ## Validate the input ##
    try:
        if isinstance(input_geojson, str) and input_geojson.endswith('.geojson'):
            with open(input_geojson) as f:
                geom = geojson.load(f) # Attempt to load the GeoJSON file
        else:
            geom = geojson.loads(input_geojson) # Attempt to parse the GeoJSON string
        return geom
    except Exception as e:
        print("Your file was unable to be processed. Please upload a valid GeoJSON string/file input.")
        return None 
    


def simplify_geometry(geom, tolerance=0.01, preserve_topology=True):
    
   # Convert to a Shapely geometry
    if 'geometry' in geom:
        shapely_geom = shape(geom['geometry'])
    else:
        print("Invalid geometry data.")
        return None

    # Simplify the geometry
    simplified = shapely_geom.simplify(tolerance, preserve_topology)

    # Convert back to GeoJSON
    output_geojson = geojson.dumps(mapping(simplified))
    return output_geojson
    

def handle_types(geom):
    
    if geom['type'] not in ['Feature', 'FeatureCollection', 'Polygon', 'MultiPolygon']:
        raise ValueError("Geometry must be a Feature or FeatureCollection.")
    
    if geom['type'] == 'FeatureCollection':
        for feature in geom['features']:
            simplified_geojson = simplify_geometry(feature)
            if simplified_geojson:
                print("A feature was successfully processed and simplified.")
                return simplified_geojson
    elif geom['type'] in ['Feature', 'Polygon', 'MultiPolygon']:
        simplified_geojson = simplify_geometry(geom)
        if simplified_geojson:
            print("Your geometry was successfully processed and simplified.")
            return simplified_geojson 
    else:
        print("Unsupported GeoJSON type.")
        return None

def output_handler(simplified):
    
    while True:
        output_format = input("Would you like to save the simplified GeoJSON as a string or file path? (Please enter either 'string' or 'file' exactly as shown): ")
        if output_format == 'string':
            print(simplified)
            break
        elif output_format == 'file':

            file_name = input("Please enter the name of the output file you wish to create: ")
            if not file_name.endswith('.geojson'):
                print("The file name must end with .geojson. Please enter a valid file name.")
                continue

            output_path = input("Please enter the file path where you wish to save the output file: ")
            if not os.path.exists(output_path):
                print("The file path is invalid.")
                continue

            output_path = os.path.join(output_path, file_name)
            with open(output_path, 'w') as f:
                f.write(simplified)
            print("Your file was successfully saved.")
            break
        else:
            print("Invalid input. Please enter either 'string' or 'file' exactly as shown: ")


def main():
    input_geojson = load_data() #load the data

    geom = validate_input(input_geojson) 
    if not geom: #validate the input
        return 1
    
    print("Your file was successfully processed.")
    simplified = handle_types(geom)
   
    if not simplified:
        return 1
    
    output_handler(simplified)
    return 0

if __name__ == "__main__":
    main()
