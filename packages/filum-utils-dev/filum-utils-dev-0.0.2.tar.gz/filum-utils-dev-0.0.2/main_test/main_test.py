import unittest

from filum_utils_dev import CampaignClient, ConnectionClient, AutomatedActionClient
from filum_utils_dev.clients.connection import get_connections_by_data_key


class TestCase(unittest.TestCase):
    def test_data_1(self):
        current_index = None
        last_current_index = 1
        print(f"Last current index not matched: {current_index} != {last_current_index}")

    def test_for_fun(self):
        subscription_id = 1671
        campaign_client = CampaignClient(subscription_id=subscription_id)

        def function_for_campaign(action, campaign, data, subscription_data, connections):
            print("ACTION")
            print(action)
            print("CAMPAIGN")
            print(campaign)
            print("DATA")
            print(data)
            print("SUBSCRIPTION DATA")
            print(subscription_data)
            print("CONNECTIONS")
            print(connections)
            print("------------------")

        campaign_client.handle_segment_users_on_demand_trigger(
            process_segment_user_fn=function_for_campaign,
            properties=["Phone"],
            required_properties=[["Phone"]],
            connections=[],
            last_current_index=0,
            dedup_key="Phone"
        )

    def test_automated_action(self):
        subscription_id = 1545
        automated_action_client = AutomatedActionClient(subscription_id)
        print(automated_action_client.automated_action)
        print(automated_action_client.get_context_type())
        print(automated_action_client.get_context_id())
        print(automated_action_client.get_subscription_data())

        custom_organization = {
            "id": "organization_id",
            "platform_url": "this_is_platform_url"
        }

        def function_for_fun(action, automated_action, data, subscription_data, connections, organization):
            # print("ACTION")
            # print(action)
            # print("AUTOMATED ACTION")
            # print(automated_action)
            # print("DATA")
            # print(data)
            # print("SUBSCRIPTION DATA")
            # print(subscription_data)
            # print("CONNECTIONS")
            # print(connections)
            # print("ORGANIZATION")
            # print(organization)
            # print("------------------")
            return True

        def function_for_on_demand(action, automated_action, data, subscription_data, connections, organization):
            # print("ON DEMAND")
            # print(connections)
            # print(organization)
            return False

        def function_for_campaign(action, campaign, data, subscription_data, connections):
            print("ACTION")
            print(action)
            print("CAMPAIGN")
            print(campaign)
            print("DATA")
            print(data)
            print("SUBSCRIPTION DATA")
            print(subscription_data)
            print("CONNECTIONS")
            print(connections)
            print("------------------")

        aa_client_1_result = automated_action_client.handle_transactional_trigger(
            process_transactional_fn=function_for_fun,
            events=[{
                "name": "Long"
            }],
            connections=[],
            organization=custom_organization
        )

        aa_client_2_result = automated_action_client.handle_object_on_demand_trigger(
            process_segment_fn=function_for_on_demand,
            organization=custom_organization
        )

        print(aa_client_1_result)
        print(aa_client_2_result)

        # campaign_client = CampaignClient(subscription_id=1053)
        # campaign_client.handle_transactional_trigger(
        #     process_transactional_fn=function_for_campaign,
        #     events=[{
        #         "name": "Long"
        #     }],
        #     connections=[{"id": 1, "name": "Connection"}]
        # )

    def test_installed_source(self):
        connections = get_connections_by_data_key(key="zalo_oa_id", value="901342586131576382")
        # 2262007475432007812
        # 901342586131576382
        print(connections)
        # connection_client = ConnectionClient(connection_id=344)
        # print(connection_client.connection.get("data"))
        # connection_client.update_data({
        #     "zalo_oa_id": "901342586131576382"
        # })
        # 901342586131576382

    def test_function(self):
        subscription_id = 829

        campaign_client = CampaignClient(subscription_id=subscription_id)

        campaign = campaign_client.campaign

        print(campaign)
        print(campaign_client.action_client.action)
        print(campaign_client.get_template_third_party_id())
        print(campaign_client.get_run_type())
        print(campaign_client.get_segment_id())

    def test_handle_trigger_failed(self):
        campaign_client = CampaignClient(subscription_id=940)

        campaign_client.handle_trigger_failed(
            error={
                "type": "external",
                "message": "Test External Error",
                "data": "",
                "notification_message": "Test External Error"
            },
            notify=True
        )
