import json
import os

def generate_game_jsons(game_data, image_paths, output_path):
    """
    Generate two JSON files: index.json and detailed metadata.
    """
    game_id = game_data["GameID"]
    game_folder = os.path.join(output_path, game_id)
    os.makedirs(game_folder, exist_ok=True)
    
    # Construct paths for images
    preview_image = os.path.join("gamesdb", game_data["Publisher"].replace(" ", "-"), game_id, "preview.webp")
    assets_images = [os.path.join("gamesdb", game_data["Publisher"].replace(" ", "-"), game_id, f"assets/image{i+1}.webp") for i in range(3)]
    icon_image = os.path.join("gamesdb", game_data["Publisher"].replace(" ", "-"), game_id, "icon.webp")
    
    # Index JSON
    index_json = {
        "GameID": game_id,
        "GameName": game_data["GameName"],
        "Publisher": game_data["Publisher"],
        "Category": game_data["Category"],
        "ShortDescription": game_data["ShortDescription"],
        "Visible": True,
        "XRated": False,
        "GameFile": os.path.join("gamesdb", game_data["Publisher"].replace(" ", "-"), game_id, "game.json"),
        "Preview": preview_image,
        "Assets": "gamesdb/{}/{}/*.webp".format(game_data["Publisher"].replace(" ", "-"), game_id),
        "Price": 0.00,
        "Blockchain": None,
        "Type": "native",
        "downloadType": "torrent",
        "Platform": 1,
        "isHyperPlayExclusive": False
    }
    
    index_json_path = os.path.join(game_folder, "index.json")
    with open(index_json_path, "w") as f:
        json.dump(index_json, f, indent=4)
    
    # Detailed Metadata JSON
    detailed_metadata = {
        "_id": game_id,
        "name": game_data["GameName"],
        "short_description": game_data["ShortDescription"],
        "description": "Experience the game in its full glory.",
        "tags": game_data["Category"],
        "type": "native",
        "gallery": assets_images,
        "price": 0.00,
        "dlcs": [],
        "updates": [],
        "platforms": {
            "windows_amd64": {
                "name": game_data["GameName"],
                "executable": f"{game_id}/{game_id}.exe",
                "installSize": "Unknown",
                "external_url": "magnet:?xt=null"
            },
            "linux_amd64": {
                "name": game_data["GameName"],
                "executable": "",
                "installSize": "",
                "external_url": "magnet:?xt=null"
            }
        },
        "system_requirements": {
            "cpu": "Unknown",
            "gpu": "Unknown",
            "disk": "Unknown",
            "memory": "Unknown"
        }
    }
    
    detailed_json_path = os.path.join(game_folder, "game.json")
    with open(detailed_json_path, "w") as f:
        json.dump(detailed_metadata, f, indent=4)
    
    print(f"✅ Generated JSON files: {index_json_path}, {detailed_json_path}")
    return [index_json_path, detailed_json_path]