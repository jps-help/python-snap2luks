# Snap2LUKS

A simple python script to convert Ubuntu TPM-backed FDE snap recovery keys to a
working LUKS key-file.

## Usage

The following example will convert the recovery key from `snap recovery` and
prompt you to create and additional passphrase, for unlocking your Ubuntu
partition from another operating system.

```bash
# Retrieve the recovery keys from "snap recovery" and create "key.out" file
# with this script.
pipx run --spec git+https://github.com/jps-help/python-snap2luks snap2luks --string "$(
  sudo snap recovery --show-keys | sed -e 's/recovery: \+//'
)"

# Add a new LUKS key to your Ubuntu partition.
#
# - Replace "nvme0n1p4" with "sda4" or an equivalent if you use a SATA drive
#   instead of an NVME drive or if your drive ist not the primary drive.
# - Replace the partition number "4" with an appropriate partition number if
#   necessary.
sudo cryptsetup luksAddKey --key-file "key.out" /dev/nvme0n1p4 

# Delete the key file.
rm "key.out"
```
