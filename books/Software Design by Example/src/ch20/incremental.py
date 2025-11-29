import json
import sys

def main():
    manifest = json.load(sys.stdin)
    packages = list(manifest.keys())
    if len(sys.argv) > 1:
        packages.reverse()

    accum = []
    count = find(manifest=manifest,
                 remaining=packages,
                 accum=accum,
                 current=[],
                 count=0,
                 )

    print(f"count {count}")
    for a in accum:
        print(a)

def find(manifest, remaining, accum, current, count):
    count += 1
    if not remaining:
        accum.append(current)
    else:
        head, tail = remaining[0], remaining[1:]
        for version in manifest[head]:
            candidate = current + [(head, version)]
            if compatible(manifest, candidate):
                count = find(
                    manifest, tail, accum, candidate, count
                )
    return count

def compatible(manifest, combination):
    for package_i, version_i in combination:
        lookup_i = manifest[package_i][version_i]
        for package_j, version_j in combination:
            if package_i == package_j:
                continue
            if package_j not in lookup_i:
                # package_i doesn't depend on package_j
                continue
            # package_i depends on packages j
            if version_j not in lookup_i[package_j]:
                # version_j doesn't satisfy the constraint :(
                return False
    return True

if __name__ == "__main__":
    main()
