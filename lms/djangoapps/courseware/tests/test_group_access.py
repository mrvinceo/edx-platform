import ddt
from django.test import TestCase
from stevedore.extension import Extension, ExtensionManager

from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from xmodule.partitions.partitions import Group, UserPartition, USER_PARTITION_SCHEME_NAMESPACE
from xmodule.modulestore.django import modulestore

import courseware.access as access
from courseware.tests.factories import UserFactory


class MemoryUserPartitionScheme(object):
    """
    In-memory partition scheme for testing.
    """
    name = "memory"

    def __init__(self):
        self.current_group = {}

    def set_group_for_user(self, user, user_partition, group):
        self.current_group.setdefault(user.id, {})[user_partition.id] = group

    def get_group_for_user(self, course_id, user, user_partition, track_function=None):  # pylint: disable=unused-argument
        """
        """
        return self.current_group.get(user.id, {}).get(user_partition.id)


UserPartition.scheme_extensions = ExtensionManager.make_test_instance(
    [
        Extension(
            "memory",
            USER_PARTITION_SCHEME_NAMESPACE,
            MemoryUserPartitionScheme(),
            None
        ),
    ],
    namespace=USER_PARTITION_SCHEME_NAMESPACE
)


@ddt.ddt
class GroupAccessTestCase(TestCase):
    """
    Tests to ensure that has_access() correctly enforces the visibility
    restrictions specified in the `group_access` field of XBlocks.
    """

    cat_group = Group(10, 'cats')
    dog_group = Group(20, 'dogs')
    animal_partition = UserPartition(
        0,
        'Pet Partition',
        'which animal are you?',
        [cat_group, dog_group],
        scheme=UserPartition.get_scheme("memory"),
    )

    red_group = Group(1000, 'red')
    blue_group = Group(2000, 'blue')
    color_partition = UserPartition(
        100,
        'Color Partition',
        'what color are you?',
        [red_group, blue_group],
        scheme=UserPartition.get_scheme("memory"),
    )

    course = CourseFactory.create(user_partitions=[animal_partition, color_partition])
    chapter = ItemFactory.create(category='chapter', parent=course)
    section = ItemFactory.create(category='sequential', parent=chapter)
    vertical = ItemFactory.create(category='vertical', parent=section)
    component = ItemFactory.create(category='problem', parent=vertical)

    ALL_BLOCKS = [chapter, section, vertical, component]
    ALL_PARENT_CHILD = [
        (chapter, section),
        (chapter, vertical),
        (chapter, component),
        (section, vertical),
        (section, component),
        (vertical, component),
    ]

    def set_user_group(self, user, partition, group):
        """
        Internal DRY / shorthand.
        """
        partition.scheme.set_group_for_user(user, partition, group)

    def set_group_access(self, block, access_dict):
        """
        DRY helper.
        """
        block.group_access = access_dict
        modulestore().update_item(block, 1)

    @classmethod
    def setUpClass(cls):
        """
        Make preliminary assertions about the default states of fixtures,
        since the tests in this class make assumptions about them.
        """
        for block in (
                cls.course,
                cls.chapter,
                cls.section,
                cls.vertical,
                cls.component
        ):
            assert(
                block.group_access is None,
                'unexpected default group access in {}: {}'.format(block, block.group_access),
            )

    def setUp(self):

        # Reset group access in fixtures.
        for block in (
                self.course,
                self.chapter,
                self.section,
                self.vertical,
                self.component
        ):
            block.group_access = None

        self.red_cat = UserFactory()  # student in red and cat groups
        self.set_user_group(self.red_cat, self.animal_partition, self.cat_group)
        self.set_user_group(self.red_cat, self.color_partition, self.red_group)

        self.blue_dog = UserFactory()  # student in blue and dog groups
        self.set_user_group(self.blue_dog, self.animal_partition, self.dog_group)
        self.set_user_group(self.blue_dog, self.color_partition, self.blue_group)

        self.gray_mouse = UserFactory()  # student in no group

    def check_access(self, user, block, is_accessible):
        """
        DRY helper.
        """
        self.assertIs(
            access.has_access(user, 'load', block, self.course.id),
            is_accessible
        )

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_single_partition_single_group(self, block):
        """
        Access checks are correctly enforced on the block when a single group
        is specified for a single partition.
        """
        self.set_group_access(block, {self.animal_partition.id: [self.cat_group.id]})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, False)
        self.check_access(self.gray_mouse, block, False)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_single_partition_two_groups(self, block):
        """
        Access checks are correctly enforced on the block when multiple groups
        are specified for a single partition.
        """
        self.set_group_access(block, {self.animal_partition.id: [self.cat_group.id, self.dog_group.id]})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, False)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_single_empty_partition(self, block):
        """
        No group access checks are enforced on the block when group_access
        declares a partition but does not specify any groups.
        """
        self.set_group_access(block, {self.animal_partition.id: []})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_empty_dict(self, block):
        """
        No group access checks are enforced on the block when group_access is an
        empty dictionary.
        """
        self.set_group_access(block, {})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_none(self, block):
        """
        No group access checks are enforced on the block when group_access is None.
        """
        self.set_group_access(block, None)
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_single_partition_group_none(self, block):
        """
        No group access checks are enforced on the block when group_access
        specifies a partition but its value is None.
        """
        self.set_group_access(block, {self.animal_partition.id: None})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_nonexistent_partition(self, block):
        """
        No group access checks are enforced on the block when group_access
        specifies a partition id that does not exist in course.user_partitions.
        """
        self.set_group_access(block, {9: []})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_has_access_nonexistent_group(self, block):
        """
        No group access checks are enforced on the block when group_access
        contains a group id that does not exist in its referenced partition.
        """
        self.set_group_access(block, {self.animal_partition.id: [99]})
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, True)
        self.check_access(self.gray_mouse, block, True)

    @ddt.data(*ALL_BLOCKS)
    def test_multiple_partitions(self, block):
        """
        Group access restrictions are correctly enforced when multiple partition
        / group rules are defined.
        """
        self.set_group_access(
            block,
            {
                self.animal_partition.id: [self.cat_group.id],
                self.color_partition.id: [self.red_group.id],
            }
        )
        self.check_access(self.red_cat, block, True)
        self.check_access(self.blue_dog, block, False)
        self.check_access(self.gray_mouse, block, False)

    @ddt.data(*ALL_BLOCKS)
    def test_multiple_partitions_deny_access(self, block):
        """
        Group access restrictions correctly deny access even when some (but not
        all) group_access rules are satisfied.
        """
        self.set_group_access(block, {
            self.animal_partition.id: [self.cat_group.id],
            self.color_partition.id: [self.blue_group.id],
        })
        self.check_access(self.red_cat, block, False)
        self.check_access(self.blue_dog, block, False)

    @ddt.data(*ALL_PARENT_CHILD)
    @ddt.unpack
    def test_merged_groups(self, parent_block, child_block):
        """
        """
        # parent is accessible to dogs and cats
        self.set_group_access(
            parent_block, {
                self.animal_partition.id: [self.cat_group.id, self.dog_group.id],
            }
        )
        # but child is accessible only to cats
        self.set_group_access(
            child_block, {
                self.animal_partition.id: [self.cat_group.id],
            }
        )

        self.assertEqual(
            access._get_merged_group_access(parent_block),
            {self.animal_partition.id: [self.cat_group.id, self.dog_group.id]},
        )
        self.assertEqual(
            access._get_merged_group_access(child_block),
            {self.animal_partition.id: [self.cat_group.id]},
        )

        self.check_access(self.red_cat, parent_block, True)
        self.check_access(self.blue_dog, parent_block, True)
        self.check_access(self.red_cat, child_block, True)
        self.check_access(self.blue_dog, child_block, False)

    @ddt.data(*ALL_PARENT_CHILD)
    @ddt.unpack
    def test_merged_partitions(self, parent_block, child_block):
        """
        """
        # parent is accessible to dogs
        self.set_group_access(
            parent_block,
            {self.animal_partition.id: [self.dog_group.id]},
        )
        # child is accessible to red
        self.set_group_access(
            child_block,
            {self.color_partition.id: [self.red_group.id]},
        )
        self.assertEqual(
            access._get_merged_group_access(parent_block),
            {self.animal_partition.id: [self.dog_group.id]},
        )
        self.assertEqual(
            access._get_merged_group_access(child_block),
            {
                self.animal_partition.id: [self.dog_group.id],
                self.color_partition.id: [self.red_group.id],
            },
        )
        self.check_access(self.red_cat, parent_block, False)
        self.check_access(self.blue_dog, parent_block, True)
        self.check_access(self.red_cat, child_block, False)
        self.check_access(self.blue_dog, child_block, False)

    @ddt.data(*ALL_PARENT_CHILD)
    @ddt.unpack
    def test_merged_disjoint(self, parent_block, child_block):
        """
        """
        # parent is accessible to dogs
        self.set_group_access(
            parent_block, {
                self.animal_partition.id: [self.dog_group.id],
            }
        )
        # child is accessible to cats
        self.set_group_access(
            child_block, {
                self.animal_partition.id: [self.cat_group.id],
            }
        )
        self.assertEqual(
            access._get_merged_group_access(parent_block),
            {self.animal_partition.id: [self.dog_group.id]},
        )
        self.assertEqual(
            access._get_merged_group_access(child_block),
            {self.animal_partition.id: False},
        )

        self.check_access(self.red_cat, parent_block, False)
        self.check_access(self.blue_dog, parent_block, True)
        self.check_access(self.red_cat, child_block, False)
        self.check_access(self.blue_dog, child_block, False)

    def test_staff_overrides_group_access(self):
        """
        Group access restrictions are waived for staff.
        """
        pass

    def test_anonymous(self):
        """
        Group access restrictions are enforced even with anonymous users.
        """
        pass

