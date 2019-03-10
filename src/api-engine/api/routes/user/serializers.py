#
# SPDX-License-Identifier: Apache-2.0
#
from rest_framework import serializers
from api.common.enums import Operation, NetworkType, FabricNodeType, UserRole
from api.common.serializers import PageQuerySerializer
from api.models import UserProfile


class NodeQuery(PageQuerySerializer):
    pass


class NodeCreateBody(serializers.Serializer):
    network_type = serializers.ChoiceField(
        help_text=NetworkType.get_info("Network types:", list_str=True),
        choices=NetworkType.to_choices(True),
    )
    type = serializers.ChoiceField(
        help_text=FabricNodeType.get_info("Node Types:", list_str=True),
        choices=FabricNodeType.to_choices(True),
    )


class NodeIDSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="ID of node")


class NodeOperationSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        help_text=Operation.get_info("Operation for node:", list_str=True),
        choices=Operation.to_choices(True),
    )


class UserCreateBody(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        help_text=UserRole.get_info("User roles:", list_str=True),
        choices=UserRole.to_choices(string_as_value=True),
    )

    class Meta:
        model = UserProfile
        fields = ("username", "role", "organization", "password", "email")
        extra_kwargs = {
            "username": {"required": True},
            "role": {"required": True},
            "password": {"required": True},
            "email": {"required": True},
        }


class UserIDSerializer(serializers.Serializer):
    id = serializers.UUIDField(help_text="ID of user")


class UserQuerySerializer(PageQuerySerializer, serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username", "page", "per_page")


class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(help_text="ID of user")

    class Meta:
        model = UserProfile
        fields = ("id", "username", "role")
        extra_kwargs = {"id": {"read_only": False}}


class UserListSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total number of users")
    data = UserInfoSerializer(many=True, help_text="Users list")


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text="Username for login", max_length=64
    )
    password = serializers.CharField(
        help_text="Password for login", max_length=64
    )


class UserAuthResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(help_text="Access token")
    expires_in = serializers.IntegerField(help_text="Expires time")
    scope = serializers.CharField(help_text="Scopes for token")
    token_type = serializers.CharField(help_text="Type of token")
