# This file is part of vaultio.
#
# vaultio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# vaultio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vaultio.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
import subprocess

from vaultio.vault.api import MACError, create_derived_secrets, decrypt_sync, download_sync
from vaultio.util import InputError, password_input

class VaultSync:

    def __init__(self, encrypted=None, email=None, password=None, provider_choice=None, provider_token=None) -> None:

        if encrypted is None:
            encrypted, derived_secrets = download_sync(email, password, provider_choice, provider_token)
        else:
            derived_secrets = create_derived_secrets(encrypted["email"], password, encrypted["kdf"])

        self.encrypted = encrypted
        self.decrypted = decrypt_sync(encrypted, derived_secrets)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def lock(self):
        self.objects = None
        return True

    def unlock(self, password=None):
        if password is None:
            password = password_input()
        derived_secrets = create_derived_secrets(self.sync["email"], password, self.sync["kdf"])
        try:
            self.objects = decrypt_sync(self.sync, derived_secrets)
            return True
        except (InputError, MACError):
            return False

    def sync(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def generate(
            self, length=None, uppercase=None, lowercase=None, numbers=None, special=None,
            passphrase=None, words=None, seperator=None, capitalize=None, include_number=None,
            ambiguous=None, min_number=None, min_special=None
    ):

        raise NotImplementedError

    def fingerprint(self):
        raise NotImplementedError

    def template(self, type):
        raise NotImplementedError

    def get_attachment(self, attachment_id, item_id):
        raise NotImplementedError

    def new_attachment(self, uuid, fpath=None):
        raise NotImplementedError

    GET_TYPES = {
        "item",
        "folder",
    }

    def get(self, uuid, type="item"):
        raise NotImplementedError

    NEW_TYPES = {
    }

    def new(self, value, type="item"):
        raise NotImplementedError

    EDIT_TYPES = {
    }

    def edit(self, value, type="item"):
        raise NotImplementedError

    DELETE_TYPES = {
    }

    def delete(self, uuid, type="item"):
        raise NotImplementedError

    def restore(self, uuid):
        raise NotImplementedError

    LIST_TYPES = {
        "item",
        "folder",
    }

    def iter_ciphers(self, type_id):
        for cipher in self.decrypted["ciphers"]:
            if cipher["type"] == type_id:
                yield cipher

    def list(self, type="item"):
        if type.rstrip("s") == "item":
            return list(self.iter_ciphers(1))
        if type.rstrip("s") == "folder":
            return list(self.decrypted["folders"])
        else:
            raise NotImplementedError

    def confirm(self, uuid, organization_id):
        raise NotImplementedError

    def move(self, item_id, organization_id, collection_ids):
        raise NotImplementedError

    def pending(self, organization_id):
        raise NotImplementedError

    def trust(self, organization_id, request_id=None):
        raise NotImplementedError

    def deny(self, organization_id, request_id=None):
        raise NotImplementedError
