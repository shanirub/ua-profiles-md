#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#
# Authors:
# - Stefan Profanter (profanter@fortiss.org)
#

import logging
import codecs
import os
from result import TestResult
logger = logging.getLogger(__name__)


testResultIconMap = {
    TestResult.ERROR: ':x:',
    TestResult.WARNING: ':warning:',
    TestResult.NOT_IMPLEMENTED: ':heavy_minus_sign:',
    TestResult.SKIPPED: ':white_circle:',
    TestResult.NOT_SUPPORTED: ':radio_button:',
    TestResult.OK: ':heavy_check_mark:',
    TestResult.BACK_TRACE: ':collision:'
}

def write_format_markdown(profiles, selection, results, outputFilePath, templateHeaderFile, templateFooterFile):

    logger.info("Writing Markdown output to file {}".format(outputFilePath))

    outfilemd = codecs.open(outputFilePath, r"w+", encoding='utf-8')
    def writemd(line):
        print(line, end='\n', file=outfilemd)

    headerFile = codecs.open(templateHeaderFile.name, "r", encoding='utf-8')
    print(headerFile.read(), file=outfilemd)
    headerFile.close()

    writemd("## Explanation\n")

    writemd("The following tables use these signs to indicate the test results:")

    writemd(" * Error = {}".format(testResultIconMap[TestResult.ERROR]))
    writemd(" * Warning = {}".format(testResultIconMap[TestResult.WARNING]))
    writemd(" * Not Implemented = {}".format(testResultIconMap[TestResult.NOT_IMPLEMENTED]))
    writemd(" * Skipped = {}".format(testResultIconMap[TestResult.SKIPPED]))
    writemd(" * Not Supported = {}".format(testResultIconMap[TestResult.NOT_SUPPORTED]))
    writemd(" * OK = {}".format(testResultIconMap[TestResult.OK]))
    writemd(" * Back Trace = {}".format(testResultIconMap[TestResult.BACK_TRACE]))

    writeSelectedUnits(writemd, selection)

    writemd("\n")

    writeAllProfiles(writemd, profiles)

    writemd("\n")

    footerFile = codecs.open(templateFooterFile.name, "r", encoding='utf-8')
    print(footerFile.read(), file=outfilemd)
    footerFile.close()

    outfilemd.flush()
    os.fsync(outfilemd)
    outfilemd.close()

def writeSelectedUnits(writemd, selection):
    writemd("\n## Summarized Results for tested Conformance Units\n")

    writemd("Tested with version: `{}`\n".format(selection.projectInfo.version))

    writemd("| Result | Conformance Group   | Conformance Unit    |")
    writemd("|--------|---------------------|---------------------|")

    for selGroup in selection.conformanceGroups:
        writemd("| {result} | {group} |  |".format(
            group=selGroup.group.name,
            result=testResultIconMap[selGroup.result.testresult]
        ))
        for selUnit in selGroup.selectedUnits:
            writemd("| {result} |  | {unit} |".format(
                unit=selUnit.unit.name,
                result=testResultIconMap[selUnit.result.testresult]
            ))

def writeAllProfiles(writemd, profiles):

    writemd("\n## Results for all Profiles and Facets\n")

    writemd("Project Info:")
    writemd(" * Type = {}".format(profiles.projectInfo.type))
    writemd(" * Profile = {}".format(profiles.projectInfo.profile))
    writemd(" * Version = {}".format(profiles.projectInfo.version))

    writemd("\n### Conformance Groups\n")

    writemd("| Result   | Conformance Group    | Conformance Unit |")
    writemd("|----------|----------------------|------------------|")

    for group in profiles.conformanceGroups:

        writemd("| {result} | {group} |  |".format(
            group=group.name,
            result=testResultIconMap[group.getResult()]
        ))

        for unit in group.conformanceUnits:
            writemd("| {result} |  | {unit} |".format(
                unit=unit.name,
                result=testResultIconMap[unit.getResult()]
            ))

    writemd("\n### Profiles and Facets\n")

    writemd(" Units writen in *italics* are optional within that profile\n\n")

    writemd("| Result   | Profile    | Type | Name |")
    writemd("|----------|------------|------|------|")

    for profile in profiles.profiles:

        writemd("| {result} | {profile} | {type} |  |".format(
            profile=profile.name,
            result=testResultIconMap[profile.getResult()],
            type="Profile" if not profile.isFacet else "Facet"
        ))

        for incUnits in profile.conformanceUnits:

            writemd("| {result} |  | Unit | {optional}{unit}{optional} |".format(
                unit=incUnits.unit.name,
                result=testResultIconMap[incUnits.unit.getResult()],
                optional='*' if incUnits.optional else ''
            ))

        for incProfile in profile.profiles:

            writemd("| {result} |  | {type} | {unit} |".format(
                unit=incProfile.name,
                result=testResultIconMap[incProfile.getResult()],
                type="Profile" if not incProfile.isFacet else "Facet"
            ))
