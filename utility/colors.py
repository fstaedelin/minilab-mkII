# Color codes
COLORS = {
    'OFF' : 0x00,
    'RED' : 0x01,
    'BLUE' : 0x10,
    'PURPLE' : 0x11,
    'GREEN' : 0x04,
    'YELLOW' : 0x05,
    'CYAN' : 0x14,
    'WHITE' : 0x7F
}

# blinking pattern for syncing
blinking_pattern = [COLORS['BLUE'],COLORS['PURPLE'],COLORS['GREEN'],COLORS['YELLOW'],COLORS['CYAN'],COLORS['WHITE'],COLORS['RED']]

# Default Pad colors
default_pad_colors = [
    [COLORS['GREEN'], COLORS['YELLOW'], COLORS['RED'], COLORS['BLUE'], COLORS['WHITE'], COLORS['WHITE'], COLORS['WHITE'], COLORS['WHITE']],
    [COLORS['GREEN'], COLORS['YELLOW'], COLORS['RED'], COLORS['BLUE'], COLORS['WHITE'], COLORS['WHITE'], COLORS['WHITE'], COLORS['WHITE']],
]

# Transport Pad colors
transport_pad_colors = [
    [COLORS['GREEN'], COLORS['RED'], COLORS['CYAN'], COLORS['CYAN'], COLORS['OFF'], COLORS['OFF'], COLORS['OFF'], COLORS['WHITE']],
    [COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE'], COLORS['BLUE']],
]