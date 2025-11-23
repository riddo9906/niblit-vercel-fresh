"""
Recipes to upgrade old hardware to modern adapters.
These are high-level blueprints; human oversight recommended.
"""
UPGRADE_RECIPES = {
    "pc_x86_legacy": {
        "replace_os": "install_minimal_linux",
        "add_bridge": "install_usb_serial_adapter",
        "notes": "Migrate services to containerized Python"
    },
    "arm_old_board": {
        "replace_os": "install_lightweight_runtime",
        "add_bridge": "check_i2c_spi_adapter",
        "notes": "Consider single-board microservice split"
    }
}
