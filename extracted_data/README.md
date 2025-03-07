# Newton TPR Extracted Data

This directory contains CSV files extracted from the Newton Traffic and Parking Regulations.

## 83 - Commercial Vehicle Restrictions

[83_commercial_vehicle_restrictions.csv](83_commercial_vehicle_restrictions.csv)

**Columns:**
- street - Street name
- start - Starting point of restriction
- end - Ending point of restriction
- vehicle_type - Type of vehicle restricted
- weight (tons) - Weight limit in tons
- time - Time periods when restriction applies
- alternate_route - Suggested alternate route
- notes - Additional information
- approval_status - Approval status

## 84 - Speed Limits

[84_speed_limits.csv](84_speed_limits.csv)

**Columns:**
- street - Street name
- direction - Direction of travel
- segment_description - Text description of segment
- start_point - Reference landmark for the start
- offset_miles - Distance from the start point
- length_miles - Length of the segment
- speed_mph - Speed limit
- notes - Additional information

## 85 - One-Way Streets

[85_one_way_streets.csv](85_one_way_streets.csv)

**Columns:**
- street - Street name
- segment_description - Text description of segment
- start - Starting point
- end - Ending point
- direction - Direction of travel
- exceptions - Vehicles or times exempted
- notes - Additional information

## 86 - U-Turns Prohibited

[86_u_turns_prohibited.csv](86_u_turns_prohibited.csv)

**Columns:**
- street - Street name
- location - Specific location of restriction
- notes - Additional information

## 87 - Left Turns Prohibited

[87_left_turns_prohibited.csv](87_left_turns_prohibited.csv)

**Columns:**
- from - Street where turn begins
- to - Street where turn ends
- direction - Direction of travel
- exceptions - Vehicles or times exempted
- times - Time periods when restriction applies
- other - Additional conditions

## 88 - Right Turn Only

[88_right_turn_only.csv](88_right_turn_only.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- notes - Additional information

## 89 - Right Turns Prohibited

[89_right_turns_prohibited.csv](89_right_turns_prohibited.csv)

**Columns:**
- from - Street where turn begins
- to - Street where turn ends
- direction - Direction of travel
- exceptions - Vehicles or times exempted
- times - Time periods when restriction applies
- notes - Additional information

## 96 - No Turn on Red

[96_no_turn_on_red.csv](96_no_turn_on_red.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- times - Time periods when restriction applies
- notes - Additional information

## 97 - Left Lane Must Turn Left

[97_left_lane_must_turn_left.csv](97_left_lane_must_turn_left.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- notes - Additional information

## 98 - Right Lane Must Turn Right

[98_right_lane_must_turn_right.csv](98_right_lane_must_turn_right.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- notes - Additional information

## 99 - Through Travel Prohibited

[99_through_travel_prohibited.csv](99_through_travel_prohibited.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- times - Time periods when restriction applies
- exceptions - Vehicles or times exempted
- notes - Additional information

## 145 - Traffic Control Signals

[145_traffic_control_signals.csv](145_traffic_control_signals.csv)

**Columns:**
- location - Intersection or location of signal
- type - Type of traffic control
- notes - Additional information

## 146 - Flashing Warning Lights

[146_flashing_warning_lights.csv](146_flashing_warning_lights.csv)

**Columns:**
- location - Intersection or location of light
- type - Type of warning light
- color - Color of light
- notes - Additional information

## 147 - Stop Signs

[147_stop_signs.csv](147_stop_signs.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- notes - Additional information

## 148 - Yield Signs

[148_yield_signs.csv](148_yield_signs.csv)

**Columns:**
- street1 - Primary street
- street2 - Intersecting street
- direction - Direction of travel
- notes - Additional information

## 149 - School Zones

[149_school_zones.csv](149_school_zones.csv)

**Columns:**
- location - Street and location description
- school - School name
- speed_limit - School zone speed limit
- notes - Additional information

## 150 - Safety Zones

[150_safety_zones.csv](150_safety_zones.csv)

**Columns:**
- location - Street and location description
- speed_limit - Safety zone speed limit
- notes - Additional information

## 172 - Loading Zones

[172_loading_zones.csv](172_loading_zones.csv)

**Columns:**
- street - Street name
- location - Specific location description
- side - Side of street
- length - Length of zone
- times - Hours of operation
- notes - Additional information

## 179 - School Drop Off Zones

[179_school_drop_off_zones.csv](179_school_drop_off_zones.csv)

**Columns:**
- school - School name
- location - Street and location
- side - Side of street
- times - Hours of operation
- notes - Additional information

## 194 - Municipal Parking Time Limits

[194_municipal_parking_time_limits.csv](194_municipal_parking_time_limits.csv)

**Columns:**
- lot_name - Parking lot name
- location - Location description
- time_limit - Maximum parking duration
- exceptions - Exemptions to the time limit
- notes - Additional information

## 199 - Fire Lanes

[199_fire_lanes.csv](199_fire_lanes.csv)

**Columns:**
- location - Street and location description
- notes - Additional information

## 200 - Accessible Parking Spaces

[200_accessible_parking_spaces.csv](200_accessible_parking_spaces.csv)

**Columns:**
- street - Street name
- location - Specific location description
- side - Side of street
- number - Number of spaces
- notes - Additional information