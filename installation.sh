#!/bin/bash

clear

# Colors
RED='\033[1;91m'
GREEN='\033[1;92m'
YELLOW='\033[1;93m'
BLUE='\033[1;94m'
CYAN='\033[1;96m'
MAGENTA='\033[1;95m'
PURPLE='\033[1;35m'
ORANGE='\033[1;33m'
NC='\033[0m'

# ASCII Header
echo -e "${BLUE}╔══════════════════════════════════════════════════╗"
echo -e "${CYAN}║${BLUE} ███████╗ ██████╗ ██████╗ ███████╗██╗  ██╗ ${CYAN}║"
echo -e "${CYAN}║${GREEN} ██╔════╝██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝ ${CYAN}║"
echo -e "${CYAN}║${YELLOW} █████╗  ██║   ██║██████╔╝█████╗   ╚███╔╝  ${CYAN}║"
echo -e "${CYAN}║${RED} ██╔══╝  ██║   ██║██╔══██╗██╔══╝   ██╔██╗  ${CYAN}║"
echo -e "${CYAN}║${MAGENTA} ██║     ╚██████╔╝██║  ██║███████╗██╔╝ ██╗ ${CYAN}║"
echo -e "${CYAN}║${PURPLE} ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ${CYAN}║"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"

# Warning
echo -e "\n${RED}╔══════════════════════════════════════════════════════════╗"
echo -e "║${YELLOW}                   WARNING - IMPORTANT NOTICE                  ║"
echo -e "║${RED}                                                              ║"
echo -e "║${YELLOW}   This software is provided for EDUCATIONAL PURPOSES ONLY.   ║"
echo -e "║${RED}   The developer and ACCsi Forex are not responsible for any    ║"
echo -e "║${RED}   misuse of this software or any consequences that may arise.  ║"
echo -e "║${YELLOW}   Use at your own risk.                                      ║"
echo -e "║${RED}                                                              ║"
echo -e "║${CYAN}   Developed by: Abdul Qadeer Gabol                            ║"
echo -e "╚══════════════════════════════════════════════════════════╝${NC}"

echo -ne "\n${YELLOW}➤ ${CYAN}Do you accept these terms? [${GREEN}1${CYAN} = Yes/${RED}2${CYAN} = No]: ${NC}"
read choice
[[ "$choice" != "1" ]] && echo -e "\n${RED}✗ Installation aborted. Terms not accepted.${NC}" && exit 1

clear

# OS Detect
if [[ $(uname -o 2>/dev/null) == *Android* ]]; then
    OS="termux"
    BIN_DIR="$PREFIX/bin"
    echo -e "${GREEN}✓ Running on ${CYAN}Termux${GREEN} (Android)${NC}"
else
    OS="ubuntu"
    BIN_DIR="/usr/local/bin"
    echo -e "${GREEN}✓ Running on ${CYAN}Ubuntu/Linux${NC}"
fi
sleep 1

# Spinner Progress Bar
show_progress() {
    local msg=$1
    local emoji=$2
    echo -ne "\n${PURPLE}${emoji} ${MAGENTA}${msg}${NC}\n"
    local bar=""
    local spin=("-" "\\" "|" "/")
    local spin_idx=0
    for i in {1..50}; do
        bar+="▓"
        printf "\r${CYAN}[${GREEN}%-50s${CYAN}] ${YELLOW}%d%% ${spin[${spin_idx}]}" "$bar" "$((2 * i))"
        ((spin_idx = (spin_idx + 1) % 4))
        sleep 0.03
    done
    echo -e "\n${GREEN}✓ Completed!${NC}"
}

# Step Log
step() {
    local emoji=$2
    echo -e "\n${YELLOW}${emoji} ➤ ${CYAN}$1${NC}"
    sleep 0.3
}

# Retry Installer
install_package() {
    local pkg="$1"
    local max_retries=3
    local attempt=1
    local success=0
    while [[ $attempt -le $max_retries ]]; do
        if [[ "$OS" == "termux" ]]; then
            pkg install -y "$pkg" 2>/dev/null && success=1 && break
        else
            sudo apt install -y "$pkg" 2>/dev/null && success=1 && break
        fi
        echo -e "${RED}⛔ Attempt $attempt failed for $pkg. Retrying...${NC}"
        ((attempt++))
        sleep 1
    done
    [[ $success -eq 1 ]] && echo -e "${GREEN}✓ $pkg installed successfully${NC}" || echo -e "${RED}✗ Failed to install $pkg${NC}"
    return $success
}

# Installation Logic
install_refine() {
    [[ "$OS" == "termux" ]] && step "Requesting Storage Permission" "📱" && termux-setup-storage && sleep 1

    step "Updating package repositories" "🔄"
    [[ "$OS" == "termux" ]] && pkg update -y >/dev/null 2>&1 || sudo apt update -y >/dev/null 2>&1

    step "Installing Python" "🐍"
    [[ "$OS" == "termux" ]] && install_package python || install_package python3 || return 1

    step "Installing Git" "🌐"
    install_package git || return 1

    step "Checking for previous installations" "🧹"
    [[ -d "Contacts-refine" ]] && echo -e "${RED}Removing old repository...${NC}" && rm -rf Contacts-refine

    step "Cloning Contacts-refine repository" "📥"
    git clone https://github.com/AbdulMods/Contacts-refine.git || return 1

    step "Creating launcher script" "🚀"
    echo -e "#!/bin/bash\ncd $(pwd)/Contacts-refine && python Refine.py" > "$BIN_DIR/refine"
    chmod +x "$BIN_DIR/refine" || return 1
    echo -e "${GREEN}✓ Launcher created at $BIN_DIR/refine${NC}"

    step "Creating required directories" "📂"
    mkdir -p "/storage/emulated/0/Qadeer/Csv"
    mkdir -p "/storage/emulated/0/Qadeer/Refined"
    echo -e "${GREEN}✓ Created directories${NC}"

    [[ "$OS" == "ubuntu" ]] && sudo apt-get clean >/dev/null

    show_progress "Finalizing installation" "⚡"
    return 0
}

# Start Process
echo -e "\n${PURPLE}🚀 Starting installation process...${NC}"
sleep 1

if install_refine; then
    echo -e "\n${GREEN}╔══════════════════════════════════════╗"
    echo -e "║          🎉 INSTALLATION SUCCESS!        ║"
    echo -e "╚══════════════════════════════════════╝${NC}"
else
    echo -e "\n${RED}╔══════════════════════════════════════╗"
    echo -e "║          ⚠️ INSTALLATION FAILED!         ║"
    echo -e "╚══════════════════════════════════════╝${NC}"
    exit 1
fi

echo -e "\n${PURPLE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo -e "┃  ${CYAN}Tool created by: ${MAGENTA}Abdul Qadeer Gabol     ┃"
echo -e "┃  ${CYAN}         (ACCsi Forex Refiner)        ┃"
echo -e "┃                                            ┃"
echo -e "┃  ${YELLOW}⚠️ ${RED}LEGAL DISCLAIMER: ${ORANGE}Use only for     ┃"
echo -e "┃  ${ORANGE}educational purposes. Owner NOT      ┃"
echo -e "┃  ${ORANGE}responsible for any misuse.          ┃"
echo -e "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛${NC}"

# Launch Prompt
if command -v refine &>/dev/null; then
    echo -e "\n${BLUE}👉 ${CYAN}Press Enter to launch the tool ${GREEN}OR"
    echo -e "${BLUE}👉 ${CYAN}Type 'refine' anytime to run it${NC}"
    read -p $'\n'"${YELLOW}➤ ${CYAN}Launch now? [${GREEN}Y${CYAN}/${RED}n${CYAN}]: ${NC}" launch
    [[ "${launch,,}" != "n" ]] && clear && echo -e "${BLUE}🚀 Launching Contacts Refiner...${NC}\n" && sleep 1 && refine
else
    echo -e "\n${RED}⚠️ Launcher not found. Try:"
    echo -e "1. Restart your terminal"
    echo -e "2. Run manually: ${CYAN}cd Contacts-refine && python Refine.py${NC}"
fi

echo -e "\n${PURPLE}✨ Thanks for using the installer! ✨${NC}"
