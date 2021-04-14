# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

import sgtk
from sgtk import TankError, LogManager

log = LogManager.get_logger(__name__)
HookBaseClass = sgtk.get_hook_baseclass()


class SceneOperation(HookBaseClass):
    """
    Hook called to perform an operation with the
    current scene
    """

    def execute(
        self,
        operation,
        file_path,
        context,
        parent_action,
        file_version,
        read_only,
        **kwargs
    ):
        """
        Main hook entry point

        :param operation:       String
                                Scene operation to perform

        :param file_path:       String
                                File path to use if the operation
                                requires it (e.g. open)

        :param context:         Context
                                The context the file operation is being
                                performed in.

        :param parent_action:   This is the action that this scene operation is
                                being executed for.  This can be one of:
                                - open_file
                                - new_file
                                - save_file_as
                                - version_up

        :param file_version:    The version/revision of the file to be opened.  If this is 'None'
                                then the latest version should be opened.

        :param read_only:       Specifies if the file should be opened read-only or not

        :returns:               Depends on operation:
                                'current_path' - Return the current scene
                                                 file path as a String
                                'reset'        - True if scene was reset to an empty
                                                 state, otherwise False
                                all others     - None
        """
        # run the base class operations
        super(SceneOperation, self).execute(operation, file_path, context,
                                            parent_action, file_version,
                                            read_only, **kwargs)

        adobe = self.parent.engine.adobe

        if operation == "current_path":
            # return the current doc path
            doc = adobe.get_active_document_path()

            if doc is None:
                # new file?
                path = ""
            else:
                path = doc

            return path

        elif operation == "open":

            # open the specified script
            adobe.app.load(adobe.File(file_path))

        elif operation == "save":
            # save the current script
            doc = self._get_active_document()
            doc.save()

        elif operation == "save_as":
            # save current script as file_path
            doc = self._get_active_document()
            adobe.save_as(doc, file_path)

        elif operation == "reset":
            # do nothing and indicate scene was reset to empty
            return True

        elif operation == "prepare_new":
            # file->new. Not sure how to pop up the actual file->new UI,
            # this command will create a document with default properties
            adobe.app.documents.add()

    def _get_active_document(self):
        """
        Returns the currently open document in Photoshop.
        Raises an exeption if no document is active.
        """
        doc = self.parent.engine.adobe.get_active_document()

        if not doc:
            raise TankError("There is no active document!")

        return doc
