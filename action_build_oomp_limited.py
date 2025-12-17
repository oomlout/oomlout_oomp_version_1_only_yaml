import action_all_default

def main(**kwargs):
    #added a comment
    action_all_default.main(**kwargs)

if __name__ == "__main__":
    kwargs = {}
    
    filter = ""
    #filter = "spacer"
    #filter = "hardware"    

    #filter = "packaging"
    #filter = "screw_socket_cap"
    #filter = "screw_self_tapping"
    #filter = ["set_screw","bolt"]
    #filter = "standoff"
    #filter = "hardware_spacer_m3_id_7_mm_od_nylon_white_25_mm_length"
    
    kwargs["filter"] = filter

    #if filter isn't a array then make it one
    if not isinstance(kwargs["filter"], list):
        kwargs["filter"] = [kwargs["filter"]]

    for f in kwargs["filter"]:
        kwargs["filter"] = f
        main(**kwargs)
    