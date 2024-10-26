import pandas as pd

class GTFSPathwayGenerator:
    def __init__(self):
        # Initialize empty DataFrames for stops and pathways
        self.stops_df = pd.DataFrame(columns=["stop_id", "stop_name", "stop_lat", "stop_lon"])
        self.pathways_df = pd.DataFrame(columns=[
            "pathway_id", "from_stop_id", "to_stop_id", "pathway_mode", "is_bidirectional",
            "length", "stair_count", "max_slope", "min_width", "signposted_as", 
            "reversed_signposted_as", "description"
        ])

    def add_stop(self, stop_id, stop_name, lat, lon):
        """Adds a stop to the GTFS stops DataFrame."""
        stop_data = {"stop_id": stop_id, "stop_name": stop_name, "stop_lat": lat, "stop_lon": lon}
        self.stops_df = pd.concat([self.stops_df, pd.DataFrame([stop_data])], ignore_index=True)

    def add_pathway(self, pathway_id, from_stop_id, to_stop_id, pathway_mode, is_bidirectional, 
                    length=None, stair_count=None, max_slope=None, min_width=None,
                    signposted_as=None, reversed_signposted_as=None, description=None):
        """Adds a pathway between stops in the pathways DataFrame."""
        pathway_data = {
            "pathway_id": pathway_id,
            "from_stop_id": from_stop_id,
            "to_stop_id": to_stop_id,
            "pathway_mode": pathway_mode,
            "is_bidirectional": is_bidirectional,
            "length": length,
            "stair_count": stair_count,
            "max_slope": max_slope,
            "min_width": min_width,
            "signposted_as": signposted_as,
            "reversed_signposted_as": reversed_signposted_as,
            "description": description
        }
        self.pathways_df = pd.concat([self.pathways_df, pd.DataFrame([pathway_data])], ignore_index=True)

    def add_standard_pathways(self):
        """Adds common pathways based on the station layout."""
        # Example pathways based on your layout
        self.add_pathway(
            "elevator_1", "floor_1", "floor_2", 4, 1, 10, 
            description="Elevator connecting Floor 1 to Floor 2, accessible for mobility assistance."
        )
        self.add_pathway(
            "escalator_3_4_to_5", "tracks_3_4", "track_5", 3, 0, 15,
            signposted_as="To Track 5", description="Escalator providing one-way access from Tracks 3/4 up to Track 5."
        )
        self.add_pathway(
            "ramp_concourse_to_track1", "concourse", "track_1", 7, 1, 30, 
            max_slope="5%", min_width=2, signposted_as="To Track 1", reversed_signposted_as="To Concourse",
            description="Ramp connecting concourse to Track 1, accessible for wheelchairs with a 5% slope."
        )
        # Add other pathways as needed

    def save_to_csv(self, directory="gtfs_output"):
        """Saves stops and pathways data to CSV files in the specified directory."""
        import os
        os.makedirs(directory, exist_ok=True)
        self.stops_df.to_csv(f"{directory}/stops.txt", index=False)
        self.pathways_df.to_csv(f"{directory}/pathways.txt", index=False)
        print(f"Files saved to {directory}")

# Example Usage
gtfs = GTFSPathwayGenerator()

# Add stops (example locations based on floor plan)
gtfs.add_stop("floor_1", "Floor 1", 40.735657, -74.172366)
gtfs.add_stop("floor_2", "Floor 2", 40.735757, -74.172266)
gtfs.add_stop("track_1", "Track 1", 40.735557, -74.172166)
gtfs.add_stop("track_5", "Track 5", 40.735157, -74.171766)
gtfs.add_stop("concourse", "Concourse", 40.735957, -74.172666)

# Add standard pathways and custom ones
gtfs.add_standard_pathways()
gtfs.add_pathway("ticket_gate_main", "main_entrance", "concourse", 5, 0, 5, 
                 signposted_as="Entry Gate", description="Fare gate at the main entrance.")

# Save to CSV
gtfs.save_to_csv()

