#   Website
#   Copyright © 2019-2020  Scrub
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

####################
# Generic exceptions
####################


class DoesNotExist(Exception):
    """
    Exception for when an ORM model does not exist.
    """

    pass


class UnableToCreate(Exception):
    """
    Exception for when an ORM model cannot be created.
    """

    pass


class UnableToUpdate(Exception):
    """
    Exception for when an ORM model cannot be updated.
    """

    pass


class UnableToDelete(Exception):
    """
    Exception for when an ORM model cannot be deleted.
    """

    pass


####################
# Account exceptions
####################


class InvalidPassword(Exception):
    """
    Exception for when an Account's password is invalid.
    """

    pass


class EmailNotConfirmed(Exception):
    """
    Exception for when an Account's email has not been confirmed.
    """

    pass


#################
# Blog exceptions
#################


class UnableToGenerateSlug(Exception):
    """
    Exception for when a slug cannot be generated.
    """

    pass
