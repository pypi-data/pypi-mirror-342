"""Processor functions"""

import datetime
import filecmp
import os

from clmgr.template import template, comments


def insert_copyright(cfg, path, ext, offset, args):
    # Define backup
    backup_file = str(path.absolute()) + ".bak"

    # Open source in read_only and backup in write mode
    with open(file=path.absolute(), encoding="utf-8", mode="r") as src_read, open(
        file=backup_file, encoding="utf-8", mode="w"
    ) as src_write:
        # Read lines from source and close it
        lines = src_read.readlines()
        src_read.close()

        # Write offset to new file
        for idx in range(len(lines)):
            if idx < offset:
                src_write.write(lines[idx])

        # Now strip the written offset lines from the source
        lines = lines[offset:]

        start = comments.get(ext).get("start")
        char = comments.get(ext).get("char")
        line = comments.get(ext).get("line")
        end = comments.get(ext).get("end")
        divider = comments.get(ext).get("divider")
        license_start = comments.get(ext).get("license").get("start")
        license_end = comments.get(ext).get("license").get("end")

        # Get header
        header_detected = 0
        if lines[0].startswith(start):
            lines = lines[1:]
            header_detected = 1

        src_write.write(start + "\n")
        legal_entities = cfg["legal"]
        legal_entities_idx = 0
        for legal in legal_entities:
            year = datetime.datetime.now().year

            if legal_entities_idx < len(legal_entities) - 1:
                year = legal_entities[legal_entities_idx + 1]["inception"]

            tmpl = template(
                cfg["format"],
                legal["inception"],
                year,
                legal["name"],
                legal["locality"],
                legal["country"],
            )
            src_write.write(line + tmpl + "\n")
            legal_entities_idx += 1

        if divider:
            src_write.write(line.rstrip() + "\n")
        if cfg["license"]["enabled"]:
            if license_start != "":
                src_write.write(line + license_start + "\n")
            if cfg["license"]["external"] is False:
                src_write.write(line + cfg["license"]["content"] + "\n")
            # TODO: Read license file
            if license_end != "":
                src_write.write(line + license_end + "\n")
            if divider:
                src_write.write(line.rstrip() + "\n")

        if header_detected == 1:
            comment_lines = 0
            for x in range(len(lines)):
                if (
                    lines[x].startswith(start) or lines[x].startswith(char)
                ) and not lines[x].startswith(end):
                    if lines[x].startswith(start):
                        src_write.write(lines[x])
                    elif lines[x].startswith(char):
                        src_write.write(start + lines[x].lstrip(start))
                    comment_lines += 1

            # Remove written user comment lines from source
            for x in range(0, comment_lines):
                lines.pop(0)
        else:
            src_write.write(end + "\n")

        # Write remaining lines
        src_write.writelines(lines)
        src_write.flush()
        src_write.close()

        # Remove original file
        os.replace(backup_file, path.absolute())


def update_copyright(cfg, path, ext, offset, args):
    # Define backup
    backup_file = str(path.absolute()) + ".bak"

    # Open source in read_only and backup in write mode
    with open(file=path.absolute(), encoding="utf-8", mode="r") as src_read, open(
        file=backup_file, encoding="utf-8", mode="w"
    ) as src_write:
        start = comments.get(ext).get("start")
        line = comments.get(ext).get("line")
        divider = comments.get(ext).get("divider")

        # Read lines from source and close it
        lines = src_read.readlines()
        src_read.close()

        # Write offset to new file
        for idx in range(len(lines)):
            if idx < offset:
                src_write.write(lines[idx])

        # Now strip the written offset lines from the source
        lines = lines[offset:]

        # Get header
        if lines[0].startswith(start):
            lines = lines[1:]
            lines.insert(0, start + "\n")

        # Get Copyright block
        # This block contains only the copyright lines
        copyright_block = []
        for x in range(len(lines)):
            if (
                lines[x].startswith(line)
                and "Copyright" in lines[x]
                and x <= args.region
            ):
                copyright_block.append(lines[x])
        # Remove the copyright block lines from the source code
        for y in copyright_block:
            lines.remove(y)

        legal_entities = cfg["legal"]
        idx = 0
        for lid in range(len(legal_entities)):
            legal = legal_entities[lid]
            year = datetime.datetime.now().year

            if lid < len(legal_entities) - 1:
                year = legal_entities[lid + 1]["inception"]

            tmpl = template(
                cfg["format"],
                legal["inception"],
                year,
                legal["name"],
                legal["locality"],
                legal["country"],
            )
            lines.insert(lid + 1, line + tmpl + "\n")
            idx = lid + 1

        # Detect license block
        if cfg["license"]["enabled"]:
            license_start = comments.get(ext).get("license").get("start")
            license_end = comments.get(ext).get("license").get("end")
            license_detected = False
            license_start_idx = 0
            license_end_idx = 0
            license_block = []  # noqa: F841
            # Search for the start of the License with the search region
            # If found record index
            # Search again for end region, this can be larger than the initial
            # search region therefor to not include the search region when searching
            # for the license termination marker
            for x in range(len(lines)):
                if license_start in lines[x] and x <= args.region:
                    license_detected = True  # We found a license block
                    license_start_idx = x  # Record the start index

            for x in range(len(lines)):
                if license_end in lines[x] and x > license_start_idx:
                    license_end_idx = x

            if license_detected:
                # TODO: Process license further if required
                license_block = lines[license_start_idx:license_end_idx]  # noqa: F841
            else:
                insert_idx = idx + 1
                if divider:
                    lines.insert(insert_idx, line.rstrip() + "\n")
                    insert_idx += 1
                lines.insert(insert_idx, line + license_start + "\n")
                if cfg["license"]["external"] is False:
                    lines.insert(
                        insert_idx + 1, line + cfg["license"]["content"] + "\n"
                    )
                # TODO: Read license file
                lines.insert(insert_idx + 2, line + license_end + "\n")

        # Writes all lines to new file
        src_write.writelines(lines)
        src_write.flush()
        src_write.close()

        result = filecmp.cmp(backup_file, path.absolute(), shallow=False)

        # Remove original file
        os.replace(backup_file, path.absolute())

        return not result


def process_lines(cfg, path, ext, lines, args):
    add = 0
    upd = 0
    utd = 0
    copyright_start = 3
    offset = 0

    try:
        # Java
        if ext.lower() == "java":
            copyright_start = 2
            offset = 0

        # Typescript
        if ext.lower() == "ts":
            copyright_start = 2
            offset = 0

        # .NET
        if ext.lower() == "cs":
            copyright_start = 2
            offset = 0

        # Python
        if ext.lower() == "py":
            copyright_start = 2
            offset = 0

        # Shell
        # TODO: Implementation
        if ext.lower() == "sh":
            copyright_start = 4
            offset = 1

        start_idx = lines[copyright_start - 1]
        if "Copyright" not in start_idx:
            insert_copyright(cfg, path, ext, offset, args)
            add += 1
        else:
            if update_copyright(cfg, path, ext, offset, args):
                upd += 1
            else:
                utd += 1
    except IndexError:
        pass

    return add, upd, utd
