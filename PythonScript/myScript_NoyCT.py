import gl
import os

dataRoot = r'/mnt/HDD1/joon/home_folders'
roiMaskFileNames = ['circle_10_mask.nii.gz', 'circle_15_mask.nii.gz', 'circle_22.5_mask.nii.gz',
                    'sphere_10_mask.nii.gz', 'sphere_15_mask.nii.gz', 'sphere_22.5_mask.nii.gz']

zCTDataDir = os.path.join(dataRoot, 'RPA_zCT', 'SUV')
zCTResultDir = os.path.join(dataRoot, 'RPA-result-zct-right_lobe3', 'processed_mask')
zCTSUVFiles = sorted(os.path.join(zCTDataDir, f) for f in os.listdir(zCTDataDir) if f.endswith('.nii.gz'))

print("zCT SUV files found:", len(zCTSUVFiles))

zCTpairs = []
for zCTFile in zCTSUVFiles:
    baseName = os.path.basename(zCTFile).replace('.nii.gz', '')
    caseResultDir = os.path.join(zCTResultDir, baseName)
    caseResultFiles = [os.path.join(caseResultDir, f) for f in roiMaskFileNames]
    caseResultFiles.insert(0, zCTFile)
    zCTpairs.append(caseResultFiles)
print("zCT pairs prepared:", len(zCTpairs))

if not hasattr(gl, 'pair_index'):
    gl.pair_index = 0

print('Showing zCT pairs first. Then yCT pairs.')
all_pairs = zCTpairs #+ yCTpairs


def load_pair():
    if gl.pair_index < 0 or gl.pair_index >= len(all_pairs):
        print(f"Error: Invalid pair index {gl.pair_index}")
        return

    pt_file, circle_ten, circle_fifteen, circle_twenty_two_point_five, sphere_ten, sphere_fifteen, sphere_twenty_two_point_five = all_pairs[gl.pair_index]
    print(f"Loading pair {gl.pair_index + 1}/{len(all_pairs)}: {os.path.basename(pt_file)}")

    gl.overlaycloseall()
    gl.loadimage(pt_file)
    gl.colorname(0, 'inverted')
    gl.minmax(0, 0.0, 5.0)
    #gl.opacity(0, 0)

    gl.overlayload(circle_ten)
    gl.colorname(1, '1red')
    gl.opacity(1, 100)
    gl.overlayload(circle_fifteen)
    gl.colorname(2, '2green')
    gl.opacity(2, 100)
    gl.overlayload(circle_twenty_two_point_five)
    gl.colorname(3, '3blue')
    gl.opacity(3, 100)
    gl.overlayload(sphere_ten)
    gl.colorname(4, '6warm')
    gl.opacity(4, 100)
    gl.overlayload(sphere_fifteen)
    gl.colorname(5, '7cool')
    gl.opacity(5, 100)
    gl.overlayload(sphere_twenty_two_point_five)
    gl.colorname(6, 'mako')
    gl.opacity(6, 100)
    #gl.orthoviewmm(0, 150, 1500)

def next_pair():
    gl.pair_index = (gl.pair_index + 1) % len(all_pairs)
    load_pair()

def previous_pair():
    gl.pair_index = (gl.pair_index - 1 + len(all_pairs)) % len(all_pairs)
    load_pair()

def jump_to(index):
    if index < 0 or index >= len(all_pairs):
        print(f"Error: Index {index} out of range (0-{len(all_pairs)-1})")
        return
    gl.pair_index = index
    load_pair()

load_pair()

