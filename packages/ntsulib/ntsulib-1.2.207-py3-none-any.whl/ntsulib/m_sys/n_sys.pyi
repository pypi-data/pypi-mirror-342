import enum

__all__ = ['get_file_bom', 'get_file_content', 'get_file_encoding', 'getPlatForm', 'n_PlatForm', 'n_PlatForm_Bit']

class n_PlatForm(enum.Enum):
    win_xp: int
    win_vista: int
    win7: int
    win8: int
    win8_1: int
    win10: int
    win11: int
    win_server: int
    linux_ubuntu: int
    linux_debian: int
    linux_centos: int
    linux_fedora: int
    linux_arch: int
    linux_gentoo: int
    linux_other: int
    mac: int
    mac_catalina: int
    mac_big_sur: int
    mac_monterey: int
    mac_ventura: int
    android: int
    ios: int
    unix: int
    unknown: int

class n_PlatForm_Bit(enum.Enum):
    x86: int
    x64: int
    arm32: int
    arm64: int
    ia64: int
    mips: int
    riscv: int
    ppc: int
    unknown: int

def getPlatForm() -> tuple[n_PlatForm, n_PlatForm_Bit]: ...
def get_file_bom(file_path): ...
def get_file_encoding(file_path, candidate_encodings=['utf-8', 'gbk', 'iso-8859-9']): ...
def get_file_content(file_path, candidate_encodings: list[str] = None): ...
