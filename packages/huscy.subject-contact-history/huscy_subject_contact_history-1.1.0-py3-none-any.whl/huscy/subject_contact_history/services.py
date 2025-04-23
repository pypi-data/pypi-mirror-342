from huscy.pseudonyms.services import get_or_create_pseudonym
from huscy.subject_contact_history.models import ContactHistoryItem


def get_contact_history(subject):
    pseudonym = get_or_create_pseudonym(subject, 'subject_contact_history.contacthistoryitem')

    return ContactHistoryItem.objects.filter(pseudonym=pseudonym.code)


def create_contact_history_item(subject, project, status, creator):
    pseudonym = get_or_create_pseudonym(subject, 'subject_contact_history.contacthistoryitem')

    return ContactHistoryItem.objects.create(
        creator=creator,
        project=project,
        pseudonym=pseudonym.code,
        status=status,
    )
