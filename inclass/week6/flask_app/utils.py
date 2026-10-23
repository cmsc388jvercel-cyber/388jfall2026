import base64


def image_to_data_uri(image_field):
    # Turn the bytes stored in Mongo into a string a browser can show in <img src="...">.
    if not image_field:
        return None
    encoded = base64.b64encode(image_field.read()).decode("utf-8")
    return f"data:image/{image_field.format.lower()};base64,{encoded}"
