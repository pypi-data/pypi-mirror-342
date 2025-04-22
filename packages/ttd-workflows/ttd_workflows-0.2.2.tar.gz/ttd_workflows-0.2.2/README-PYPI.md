# ttd-workflows-python

<!-- Start Summary [summary] -->
## Summary

Workflows API: A RESTful service for commonly used workflows.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [ttd-workflows-python](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#ttd-workflows-python)
  * [SDK Installation](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#authentication)
  * [Available Resources and Operations](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#retries)
  * [Error Handling](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#error-handling)
  * [Server Selection](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#custom-http-client)
  * [Resource Management](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#resource-management)
  * [Debugging](https://github.com/thetradedesk/ttd-workflows-python/blob/master/#debugging)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install ttd-workflows
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add ttd-workflows
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from ttd-workflows python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "ttd-workflows",
# ]
# ///

from ttd_workflows import Workflows

sdk = Workflows(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import parse_datetime


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.campaign.create(request={
        "campaign_create_workflow_primary_input": {
            "advertiser_id": "<id>",
            "name": "<value>",
            "description": "yuck vice between gee ugh ha",
            "time_zone": "Pacific/Chuuk",
            "custom_cpa_click_weight": 7804.86,
            "custom_cpa_viewthrough_weight": 7602.59,
            "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
            "impressions_only_budgeting_cpm": 4492.21,
            "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
            "budget": {
                "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                "budget_in_advertiser_currency": 934.7,
                "budget_in_impressions": 491427,
                "daily_target_in_advertiser_currency": 4904.2,
                "daily_target_in_impressions": 325463,
            },
            "primary_goal": {
                "maximize_reach": False,
                "maximize_ltv_incremental_reach": True,
                "cpc_in_advertiser_currency": 1296.63,
                "ctr_in_percent": 2881.04,
                "nielsen_otp_in_percent": 5833.53,
                "cpa_in_advertiser_currency": 5193.59,
                "return_on_ad_spend_percent": 3259.9,
                "vcr_in_percent": 4078.33,
                "viewability_in_percent": 1012.51,
                "vcpm_in_advertiser_currency": 1884.35,
                "cpcv_in_advertiser_currency": 8133.97,
                "miaozhen_otp_in_percent": 8891.64,
            },
            "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
            "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
            "seed_id": "<id>",
            "campaign_conversion_reporting_columns": [
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 17207,
                    "roas_config": {
                        "include_in_custom_roas": True,
                        "custom_roas_weight": 8441.62,
                        "custom_roas_click_weight": 3535.31,
                        "custom_roas_viewthrough_weight": 4287.45,
                    },
                    "weight": 6798.85,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": True,
                    "reporting_column_id": 860420,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 5665.12,
                        "custom_roas_click_weight": 2955.58,
                        "custom_roas_viewthrough_weight": 2032.57,
                    },
                    "weight": 4332.24,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 995852,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 2127.75,
                        "custom_roas_click_weight": 6207.47,
                        "custom_roas_viewthrough_weight": 2841.2,
                    },
                    "weight": 6083.84,
                    "cross_device_attribution_model_id": "<id>",
                },
            ],
        },
        "campaign_create_advanced_input": {
            "flights": [
                {
                    "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                    "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                    "budget_in_advertiser_currency": 5200.49,
                    "budget_in_impressions": 728836,
                    "daily_target_in_advertiser_currency": 8007.59,
                    "daily_target_in_impressions": 117747,
                },
            ],
            "purchase_order_number": "<value>",
        },
        "ad_groups": [
            {
                "name": "<value>",
                "is_enabled": False,
                "description": "simple ouch when pfft ah",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 6290.63,
                    "budget_in_impressions": 784768,
                    "daily_target_in_advertiser_currency": 3385.24,
                    "daily_target_in_impressions": 913221,
                },
                "base_bid_cpm_in_advertiser_currency": 1541.5,
                "max_bid_cpm_in_advertiser_currency": 7218.8,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": False,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        257762,
                    ],
                    "recency_exclusion_window_in_minutes": 982866,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 3831.56,
                    "ctr_in_percent": 5720.12,
                    "nielsen_otp_in_percent": 9789.08,
                    "cpa_in_advertiser_currency": 1850.76,
                    "return_on_ad_spend_percent": 6168.92,
                    "vcr_in_percent": 9775.91,
                    "viewability_in_percent": 1909.73,
                    "vcpm_in_advertiser_currency": 3141.79,
                    "cpcv_in_advertiser_currency": 8272.61,
                    "miaozhen_otp_in_percent": 7609.47,
                },
                "creative_ids": [
                    "<value>",
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": False,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                            "budget_in_advertiser_currency": 4285.01,
                            "budget_in_impressions": 838181,
                            "daily_target_in_advertiser_currency": 9525.44,
                            "daily_target_in_impressions": 188907,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 8833.21,
                            "budget_in_impressions": 892770,
                            "daily_target_in_advertiser_currency": 1993.11,
                            "daily_target_in_impressions": 564854,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 7458.53,
                            "budget_in_impressions": 290123,
                            "daily_target_in_advertiser_currency": 700.72,
                            "daily_target_in_impressions": 547483,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": False,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 695413,
                        "demographic_member_ids": [
                            261757,
                        ],
                        "mobile_demographic_member_ids": [
                            400422,
                            257433,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [],
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": False,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                        "gender": ttd_workflows.TargetingGender.BOTH,
                        "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                        "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                        "countries": [
                            "<value>",
                            "<value>",
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 557925,
                            "frequency_goal": 643654,
                            "reset_interval_in_minutes": 700013,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 770948,
                            "frequency_goal": 347880,
                            "reset_interval_in_minutes": 698997,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 620608,
                            "frequency_goal": 546216,
                            "reset_interval_in_minutes": 500290,
                        },
                    ],
                },
            },
            {
                "name": "<value>",
                "is_enabled": True,
                "description": "satisfy majority pace however crocodile yowza",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.FIXED,
                    "budget_in_advertiser_currency": 2032.81,
                    "budget_in_impressions": 778234,
                    "daily_target_in_advertiser_currency": 4040.62,
                    "daily_target_in_impressions": 421607,
                },
                "base_bid_cpm_in_advertiser_currency": 9476.87,
                "max_bid_cpm_in_advertiser_currency": 703.96,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": False,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        426375,
                    ],
                    "recency_exclusion_window_in_minutes": 306126,
                    "target_trackable_users_enabled": False,
                    "use_mc_id_as_primary": False,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 4735.88,
                    "ctr_in_percent": 9915.94,
                    "nielsen_otp_in_percent": 4475.13,
                    "cpa_in_advertiser_currency": 5150.66,
                    "return_on_ad_spend_percent": 7248.87,
                    "vcr_in_percent": 9972.42,
                    "viewability_in_percent": 6545.2,
                    "vcpm_in_advertiser_currency": 7746.63,
                    "cpcv_in_advertiser_currency": 6813.67,
                    "miaozhen_otp_in_percent": 9625.35,
                },
                "creative_ids": [
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 87.86,
                            "budget_in_impressions": 992162,
                            "daily_target_in_advertiser_currency": 6912.82,
                            "daily_target_in_impressions": 856665,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 2102.57,
                            "budget_in_impressions": 784309,
                            "daily_target_in_advertiser_currency": 9390.93,
                            "daily_target_in_impressions": 704061,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 6477.52,
                            "budget_in_impressions": 511670,
                            "daily_target_in_advertiser_currency": 4530.79,
                            "daily_target_in_impressions": 275977,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": True,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 610092,
                        "demographic_member_ids": [
                            909366,
                            209538,
                        ],
                        "mobile_demographic_member_ids": [
                            493315,
                            778851,
                            468734,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": True,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                        "gender": ttd_workflows.TargetingGender.MALE,
                        "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                        "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                        "countries": [
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 637441,
                            "frequency_goal": 855423,
                            "reset_interval_in_minutes": 967917,
                        },
                    ],
                },
            },
        ],
        "validation_only": False,
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import parse_datetime

async def main():

    async with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:

        res = await workflows.campaign.create_async(request={
            "campaign_create_workflow_primary_input": {
                "advertiser_id": "<id>",
                "name": "<value>",
                "description": "yuck vice between gee ugh ha",
                "time_zone": "Pacific/Chuuk",
                "custom_cpa_click_weight": 7804.86,
                "custom_cpa_viewthrough_weight": 7602.59,
                "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
                "impressions_only_budgeting_cpm": 4492.21,
                "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
                "budget": {
                    "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                    "budget_in_advertiser_currency": 934.7,
                    "budget_in_impressions": 491427,
                    "daily_target_in_advertiser_currency": 4904.2,
                    "daily_target_in_impressions": 325463,
                },
                "primary_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 1296.63,
                    "ctr_in_percent": 2881.04,
                    "nielsen_otp_in_percent": 5833.53,
                    "cpa_in_advertiser_currency": 5193.59,
                    "return_on_ad_spend_percent": 3259.9,
                    "vcr_in_percent": 4078.33,
                    "viewability_in_percent": 1012.51,
                    "vcpm_in_advertiser_currency": 1884.35,
                    "cpcv_in_advertiser_currency": 8133.97,
                    "miaozhen_otp_in_percent": 8891.64,
                },
                "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
                "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
                "seed_id": "<id>",
                "campaign_conversion_reporting_columns": [
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": False,
                        "reporting_column_id": 17207,
                        "roas_config": {
                            "include_in_custom_roas": True,
                            "custom_roas_weight": 8441.62,
                            "custom_roas_click_weight": 3535.31,
                            "custom_roas_viewthrough_weight": 4287.45,
                        },
                        "weight": 6798.85,
                        "cross_device_attribution_model_id": "<id>",
                    },
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": True,
                        "reporting_column_id": 860420,
                        "roas_config": {
                            "include_in_custom_roas": False,
                            "custom_roas_weight": 5665.12,
                            "custom_roas_click_weight": 2955.58,
                            "custom_roas_viewthrough_weight": 2032.57,
                        },
                        "weight": 4332.24,
                        "cross_device_attribution_model_id": "<id>",
                    },
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": False,
                        "reporting_column_id": 995852,
                        "roas_config": {
                            "include_in_custom_roas": False,
                            "custom_roas_weight": 2127.75,
                            "custom_roas_click_weight": 6207.47,
                            "custom_roas_viewthrough_weight": 2841.2,
                        },
                        "weight": 6083.84,
                        "cross_device_attribution_model_id": "<id>",
                    },
                ],
            },
            "campaign_create_advanced_input": {
                "flights": [
                    {
                        "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                        "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                        "budget_in_advertiser_currency": 5200.49,
                        "budget_in_impressions": 728836,
                        "daily_target_in_advertiser_currency": 8007.59,
                        "daily_target_in_impressions": 117747,
                    },
                ],
                "purchase_order_number": "<value>",
            },
            "ad_groups": [
                {
                    "name": "<value>",
                    "is_enabled": False,
                    "description": "simple ouch when pfft ah",
                    "programmatic_guaranteed_private_contract_id": "<id>",
                    "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                    "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                    "budget": {
                        "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                        "budget_in_advertiser_currency": 6290.63,
                        "budget_in_impressions": 784768,
                        "daily_target_in_advertiser_currency": 3385.24,
                        "daily_target_in_impressions": 913221,
                    },
                    "base_bid_cpm_in_advertiser_currency": 1541.5,
                    "max_bid_cpm_in_advertiser_currency": 7218.8,
                    "audience_targeting": {
                        "audience_id": "<id>",
                        "audience_accelerator_exclusions_enabled": False,
                        "audience_booster_enabled": False,
                        "audience_excluder_enabled": True,
                        "audience_predictor_enabled": False,
                        "cross_device_vendor_list_for_audience": [
                            257762,
                        ],
                        "recency_exclusion_window_in_minutes": 982866,
                        "target_trackable_users_enabled": True,
                        "use_mc_id_as_primary": True,
                    },
                    "roi_goal": {
                        "maximize_reach": False,
                        "maximize_ltv_incremental_reach": True,
                        "cpc_in_advertiser_currency": 3831.56,
                        "ctr_in_percent": 5720.12,
                        "nielsen_otp_in_percent": 9789.08,
                        "cpa_in_advertiser_currency": 1850.76,
                        "return_on_ad_spend_percent": 6168.92,
                        "vcr_in_percent": 9775.91,
                        "viewability_in_percent": 1909.73,
                        "vcpm_in_advertiser_currency": 3141.79,
                        "cpcv_in_advertiser_currency": 8272.61,
                        "miaozhen_otp_in_percent": 7609.47,
                    },
                    "creative_ids": [
                        "<value>",
                        "<value>",
                    ],
                    "associated_bid_lists": [
                        {
                            "bid_list_id": "<id>",
                            "is_enabled": False,
                            "is_default_for_dimension": False,
                        },
                    ],
                    "advanced_settings": {
                        "flights": [
                            {
                                "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                                "budget_in_advertiser_currency": 4285.01,
                                "budget_in_impressions": 838181,
                                "daily_target_in_advertiser_currency": 9525.44,
                                "daily_target_in_impressions": 188907,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.FIXED,
                                "budget_in_advertiser_currency": 8833.21,
                                "budget_in_impressions": 892770,
                                "daily_target_in_advertiser_currency": 1993.11,
                                "daily_target_in_impressions": 564854,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 7458.53,
                                "budget_in_impressions": 290123,
                                "daily_target_in_advertiser_currency": 700.72,
                                "daily_target_in_impressions": 547483,
                            },
                        ],
                        "koa_optimization_settings": {
                            "are_future_koa_features_enabled": False,
                            "predictive_clearing_enabled": False,
                        },
                        "comscore_settings": {
                            "is_enabled": True,
                            "population_id": 695413,
                            "demographic_member_ids": [
                                261757,
                            ],
                            "mobile_demographic_member_ids": [
                                400422,
                                257433,
                            ],
                        },
                        "contract_targeting": {
                            "allow_open_market_bidding_when_targeting_contracts": True,
                        },
                        "dimensional_bidding_auto_optimization_settings": [
                            [],
                            [
                                ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                            ],
                        ],
                        "is_use_clicks_as_conversions_enabled": False,
                        "is_use_secondary_conversions_enabled": True,
                        "nielsen_tracking_attributes": {
                            "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                            "gender": ttd_workflows.TargetingGender.BOTH,
                            "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                            "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                            "countries": [
                                "<value>",
                                "<value>",
                                "<value>",
                            ],
                        },
                        "new_frequency_configs": [
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 557925,
                                "frequency_goal": 643654,
                                "reset_interval_in_minutes": 700013,
                            },
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 770948,
                                "frequency_goal": 347880,
                                "reset_interval_in_minutes": 698997,
                            },
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 620608,
                                "frequency_goal": 546216,
                                "reset_interval_in_minutes": 500290,
                            },
                        ],
                    },
                },
                {
                    "name": "<value>",
                    "is_enabled": True,
                    "description": "satisfy majority pace however crocodile yowza",
                    "programmatic_guaranteed_private_contract_id": "<id>",
                    "channel": ttd_workflows.AdGroupChannel.VIDEO,
                    "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                    "budget": {
                        "allocation_type": ttd_workflows.AllocationType.FIXED,
                        "budget_in_advertiser_currency": 2032.81,
                        "budget_in_impressions": 778234,
                        "daily_target_in_advertiser_currency": 4040.62,
                        "daily_target_in_impressions": 421607,
                    },
                    "base_bid_cpm_in_advertiser_currency": 9476.87,
                    "max_bid_cpm_in_advertiser_currency": 703.96,
                    "audience_targeting": {
                        "audience_id": "<id>",
                        "audience_accelerator_exclusions_enabled": True,
                        "audience_booster_enabled": False,
                        "audience_excluder_enabled": False,
                        "audience_predictor_enabled": False,
                        "cross_device_vendor_list_for_audience": [
                            426375,
                        ],
                        "recency_exclusion_window_in_minutes": 306126,
                        "target_trackable_users_enabled": False,
                        "use_mc_id_as_primary": False,
                    },
                    "roi_goal": {
                        "maximize_reach": False,
                        "maximize_ltv_incremental_reach": True,
                        "cpc_in_advertiser_currency": 4735.88,
                        "ctr_in_percent": 9915.94,
                        "nielsen_otp_in_percent": 4475.13,
                        "cpa_in_advertiser_currency": 5150.66,
                        "return_on_ad_spend_percent": 7248.87,
                        "vcr_in_percent": 9972.42,
                        "viewability_in_percent": 6545.2,
                        "vcpm_in_advertiser_currency": 7746.63,
                        "cpcv_in_advertiser_currency": 6813.67,
                        "miaozhen_otp_in_percent": 9625.35,
                    },
                    "creative_ids": [
                        "<value>",
                    ],
                    "associated_bid_lists": [
                        {
                            "bid_list_id": "<id>",
                            "is_enabled": False,
                            "is_default_for_dimension": True,
                        },
                    ],
                    "advanced_settings": {
                        "flights": [
                            {
                                "allocation_type": ttd_workflows.AllocationType.FIXED,
                                "budget_in_advertiser_currency": 87.86,
                                "budget_in_impressions": 992162,
                                "daily_target_in_advertiser_currency": 6912.82,
                                "daily_target_in_impressions": 856665,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 2102.57,
                                "budget_in_impressions": 784309,
                                "daily_target_in_advertiser_currency": 9390.93,
                                "daily_target_in_impressions": 704061,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 6477.52,
                                "budget_in_impressions": 511670,
                                "daily_target_in_advertiser_currency": 4530.79,
                                "daily_target_in_impressions": 275977,
                            },
                        ],
                        "koa_optimization_settings": {
                            "are_future_koa_features_enabled": False,
                            "predictive_clearing_enabled": True,
                        },
                        "comscore_settings": {
                            "is_enabled": True,
                            "population_id": 610092,
                            "demographic_member_ids": [
                                909366,
                                209538,
                            ],
                            "mobile_demographic_member_ids": [
                                493315,
                                778851,
                                468734,
                            ],
                        },
                        "contract_targeting": {
                            "allow_open_market_bidding_when_targeting_contracts": True,
                        },
                        "dimensional_bidding_auto_optimization_settings": [
                            [
                                ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                            ],
                        ],
                        "is_use_clicks_as_conversions_enabled": True,
                        "is_use_secondary_conversions_enabled": True,
                        "nielsen_tracking_attributes": {
                            "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                            "gender": ttd_workflows.TargetingGender.MALE,
                            "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                            "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                            "countries": [
                                "<value>",
                            ],
                        },
                        "new_frequency_configs": [
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 637441,
                                "frequency_goal": 855423,
                                "reset_interval_in_minutes": 967917,
                            },
                        ],
                    },
                },
            ],
            "validation_only": False,
        })

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name       | Type   | Scheme  | Environment Variable |
| ---------- | ------ | ------- | -------------------- |
| `ttd_auth` | apiKey | API key | `WORKFLOWS_TTD_AUTH` |

To authenticate with the API the `ttd_auth` parameter must be set when initializing the SDK client instance. For example:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import parse_datetime


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.campaign.create(request={
        "campaign_create_workflow_primary_input": {
            "advertiser_id": "<id>",
            "name": "<value>",
            "description": "yuck vice between gee ugh ha",
            "time_zone": "Pacific/Chuuk",
            "custom_cpa_click_weight": 7804.86,
            "custom_cpa_viewthrough_weight": 7602.59,
            "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
            "impressions_only_budgeting_cpm": 4492.21,
            "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
            "budget": {
                "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                "budget_in_advertiser_currency": 934.7,
                "budget_in_impressions": 491427,
                "daily_target_in_advertiser_currency": 4904.2,
                "daily_target_in_impressions": 325463,
            },
            "primary_goal": {
                "maximize_reach": False,
                "maximize_ltv_incremental_reach": True,
                "cpc_in_advertiser_currency": 1296.63,
                "ctr_in_percent": 2881.04,
                "nielsen_otp_in_percent": 5833.53,
                "cpa_in_advertiser_currency": 5193.59,
                "return_on_ad_spend_percent": 3259.9,
                "vcr_in_percent": 4078.33,
                "viewability_in_percent": 1012.51,
                "vcpm_in_advertiser_currency": 1884.35,
                "cpcv_in_advertiser_currency": 8133.97,
                "miaozhen_otp_in_percent": 8891.64,
            },
            "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
            "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
            "seed_id": "<id>",
            "campaign_conversion_reporting_columns": [
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 17207,
                    "roas_config": {
                        "include_in_custom_roas": True,
                        "custom_roas_weight": 8441.62,
                        "custom_roas_click_weight": 3535.31,
                        "custom_roas_viewthrough_weight": 4287.45,
                    },
                    "weight": 6798.85,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": True,
                    "reporting_column_id": 860420,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 5665.12,
                        "custom_roas_click_weight": 2955.58,
                        "custom_roas_viewthrough_weight": 2032.57,
                    },
                    "weight": 4332.24,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 995852,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 2127.75,
                        "custom_roas_click_weight": 6207.47,
                        "custom_roas_viewthrough_weight": 2841.2,
                    },
                    "weight": 6083.84,
                    "cross_device_attribution_model_id": "<id>",
                },
            ],
        },
        "campaign_create_advanced_input": {
            "flights": [
                {
                    "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                    "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                    "budget_in_advertiser_currency": 5200.49,
                    "budget_in_impressions": 728836,
                    "daily_target_in_advertiser_currency": 8007.59,
                    "daily_target_in_impressions": 117747,
                },
            ],
            "purchase_order_number": "<value>",
        },
        "ad_groups": [
            {
                "name": "<value>",
                "is_enabled": False,
                "description": "simple ouch when pfft ah",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 6290.63,
                    "budget_in_impressions": 784768,
                    "daily_target_in_advertiser_currency": 3385.24,
                    "daily_target_in_impressions": 913221,
                },
                "base_bid_cpm_in_advertiser_currency": 1541.5,
                "max_bid_cpm_in_advertiser_currency": 7218.8,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": False,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        257762,
                    ],
                    "recency_exclusion_window_in_minutes": 982866,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 3831.56,
                    "ctr_in_percent": 5720.12,
                    "nielsen_otp_in_percent": 9789.08,
                    "cpa_in_advertiser_currency": 1850.76,
                    "return_on_ad_spend_percent": 6168.92,
                    "vcr_in_percent": 9775.91,
                    "viewability_in_percent": 1909.73,
                    "vcpm_in_advertiser_currency": 3141.79,
                    "cpcv_in_advertiser_currency": 8272.61,
                    "miaozhen_otp_in_percent": 7609.47,
                },
                "creative_ids": [
                    "<value>",
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": False,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                            "budget_in_advertiser_currency": 4285.01,
                            "budget_in_impressions": 838181,
                            "daily_target_in_advertiser_currency": 9525.44,
                            "daily_target_in_impressions": 188907,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 8833.21,
                            "budget_in_impressions": 892770,
                            "daily_target_in_advertiser_currency": 1993.11,
                            "daily_target_in_impressions": 564854,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 7458.53,
                            "budget_in_impressions": 290123,
                            "daily_target_in_advertiser_currency": 700.72,
                            "daily_target_in_impressions": 547483,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": False,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 695413,
                        "demographic_member_ids": [
                            261757,
                        ],
                        "mobile_demographic_member_ids": [
                            400422,
                            257433,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [],
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": False,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                        "gender": ttd_workflows.TargetingGender.BOTH,
                        "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                        "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                        "countries": [
                            "<value>",
                            "<value>",
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 557925,
                            "frequency_goal": 643654,
                            "reset_interval_in_minutes": 700013,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 770948,
                            "frequency_goal": 347880,
                            "reset_interval_in_minutes": 698997,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 620608,
                            "frequency_goal": 546216,
                            "reset_interval_in_minutes": 500290,
                        },
                    ],
                },
            },
            {
                "name": "<value>",
                "is_enabled": True,
                "description": "satisfy majority pace however crocodile yowza",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.FIXED,
                    "budget_in_advertiser_currency": 2032.81,
                    "budget_in_impressions": 778234,
                    "daily_target_in_advertiser_currency": 4040.62,
                    "daily_target_in_impressions": 421607,
                },
                "base_bid_cpm_in_advertiser_currency": 9476.87,
                "max_bid_cpm_in_advertiser_currency": 703.96,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": False,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        426375,
                    ],
                    "recency_exclusion_window_in_minutes": 306126,
                    "target_trackable_users_enabled": False,
                    "use_mc_id_as_primary": False,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 4735.88,
                    "ctr_in_percent": 9915.94,
                    "nielsen_otp_in_percent": 4475.13,
                    "cpa_in_advertiser_currency": 5150.66,
                    "return_on_ad_spend_percent": 7248.87,
                    "vcr_in_percent": 9972.42,
                    "viewability_in_percent": 6545.2,
                    "vcpm_in_advertiser_currency": 7746.63,
                    "cpcv_in_advertiser_currency": 6813.67,
                    "miaozhen_otp_in_percent": 9625.35,
                },
                "creative_ids": [
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 87.86,
                            "budget_in_impressions": 992162,
                            "daily_target_in_advertiser_currency": 6912.82,
                            "daily_target_in_impressions": 856665,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 2102.57,
                            "budget_in_impressions": 784309,
                            "daily_target_in_advertiser_currency": 9390.93,
                            "daily_target_in_impressions": 704061,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 6477.52,
                            "budget_in_impressions": 511670,
                            "daily_target_in_advertiser_currency": 4530.79,
                            "daily_target_in_impressions": 275977,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": True,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 610092,
                        "demographic_member_ids": [
                            909366,
                            209538,
                        ],
                        "mobile_demographic_member_ids": [
                            493315,
                            778851,
                            468734,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": True,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                        "gender": ttd_workflows.TargetingGender.MALE,
                        "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                        "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                        "countries": [
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 637441,
                            "frequency_goal": 855423,
                            "reset_interval_in_minutes": 967917,
                        },
                    ],
                },
            },
        ],
        "validation_only": False,
    })

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [campaign](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md)

* [create](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#create) - Create a new campaign with required fields
* [post_campaign_bulk](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#post_campaign_bulk) - Create a new campaign with required fields
* [get_version](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/campaign/README.md#get_version) - GET a campaign's version

### [graphql](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/graphql/README.md)

* [execute](https://github.com/thetradedesk/ttd-workflows-python/blob/master/docs/sdks/graphql/README.md#execute) - An endpoint that executes valid GraphQL queries.


</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import BackoffStrategy, RetryConfig, parse_datetime


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.campaign.create(request={
        "campaign_create_workflow_primary_input": {
            "advertiser_id": "<id>",
            "name": "<value>",
            "description": "yuck vice between gee ugh ha",
            "time_zone": "Pacific/Chuuk",
            "custom_cpa_click_weight": 7804.86,
            "custom_cpa_viewthrough_weight": 7602.59,
            "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
            "impressions_only_budgeting_cpm": 4492.21,
            "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
            "budget": {
                "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                "budget_in_advertiser_currency": 934.7,
                "budget_in_impressions": 491427,
                "daily_target_in_advertiser_currency": 4904.2,
                "daily_target_in_impressions": 325463,
            },
            "primary_goal": {
                "maximize_reach": False,
                "maximize_ltv_incremental_reach": True,
                "cpc_in_advertiser_currency": 1296.63,
                "ctr_in_percent": 2881.04,
                "nielsen_otp_in_percent": 5833.53,
                "cpa_in_advertiser_currency": 5193.59,
                "return_on_ad_spend_percent": 3259.9,
                "vcr_in_percent": 4078.33,
                "viewability_in_percent": 1012.51,
                "vcpm_in_advertiser_currency": 1884.35,
                "cpcv_in_advertiser_currency": 8133.97,
                "miaozhen_otp_in_percent": 8891.64,
            },
            "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
            "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
            "seed_id": "<id>",
            "campaign_conversion_reporting_columns": [
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 17207,
                    "roas_config": {
                        "include_in_custom_roas": True,
                        "custom_roas_weight": 8441.62,
                        "custom_roas_click_weight": 3535.31,
                        "custom_roas_viewthrough_weight": 4287.45,
                    },
                    "weight": 6798.85,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": True,
                    "reporting_column_id": 860420,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 5665.12,
                        "custom_roas_click_weight": 2955.58,
                        "custom_roas_viewthrough_weight": 2032.57,
                    },
                    "weight": 4332.24,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 995852,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 2127.75,
                        "custom_roas_click_weight": 6207.47,
                        "custom_roas_viewthrough_weight": 2841.2,
                    },
                    "weight": 6083.84,
                    "cross_device_attribution_model_id": "<id>",
                },
            ],
        },
        "campaign_create_advanced_input": {
            "flights": [
                {
                    "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                    "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                    "budget_in_advertiser_currency": 5200.49,
                    "budget_in_impressions": 728836,
                    "daily_target_in_advertiser_currency": 8007.59,
                    "daily_target_in_impressions": 117747,
                },
            ],
            "purchase_order_number": "<value>",
        },
        "ad_groups": [
            {
                "name": "<value>",
                "is_enabled": False,
                "description": "simple ouch when pfft ah",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 6290.63,
                    "budget_in_impressions": 784768,
                    "daily_target_in_advertiser_currency": 3385.24,
                    "daily_target_in_impressions": 913221,
                },
                "base_bid_cpm_in_advertiser_currency": 1541.5,
                "max_bid_cpm_in_advertiser_currency": 7218.8,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": False,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        257762,
                    ],
                    "recency_exclusion_window_in_minutes": 982866,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 3831.56,
                    "ctr_in_percent": 5720.12,
                    "nielsen_otp_in_percent": 9789.08,
                    "cpa_in_advertiser_currency": 1850.76,
                    "return_on_ad_spend_percent": 6168.92,
                    "vcr_in_percent": 9775.91,
                    "viewability_in_percent": 1909.73,
                    "vcpm_in_advertiser_currency": 3141.79,
                    "cpcv_in_advertiser_currency": 8272.61,
                    "miaozhen_otp_in_percent": 7609.47,
                },
                "creative_ids": [
                    "<value>",
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": False,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                            "budget_in_advertiser_currency": 4285.01,
                            "budget_in_impressions": 838181,
                            "daily_target_in_advertiser_currency": 9525.44,
                            "daily_target_in_impressions": 188907,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 8833.21,
                            "budget_in_impressions": 892770,
                            "daily_target_in_advertiser_currency": 1993.11,
                            "daily_target_in_impressions": 564854,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 7458.53,
                            "budget_in_impressions": 290123,
                            "daily_target_in_advertiser_currency": 700.72,
                            "daily_target_in_impressions": 547483,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": False,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 695413,
                        "demographic_member_ids": [
                            261757,
                        ],
                        "mobile_demographic_member_ids": [
                            400422,
                            257433,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [],
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": False,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                        "gender": ttd_workflows.TargetingGender.BOTH,
                        "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                        "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                        "countries": [
                            "<value>",
                            "<value>",
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 557925,
                            "frequency_goal": 643654,
                            "reset_interval_in_minutes": 700013,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 770948,
                            "frequency_goal": 347880,
                            "reset_interval_in_minutes": 698997,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 620608,
                            "frequency_goal": 546216,
                            "reset_interval_in_minutes": 500290,
                        },
                    ],
                },
            },
            {
                "name": "<value>",
                "is_enabled": True,
                "description": "satisfy majority pace however crocodile yowza",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.FIXED,
                    "budget_in_advertiser_currency": 2032.81,
                    "budget_in_impressions": 778234,
                    "daily_target_in_advertiser_currency": 4040.62,
                    "daily_target_in_impressions": 421607,
                },
                "base_bid_cpm_in_advertiser_currency": 9476.87,
                "max_bid_cpm_in_advertiser_currency": 703.96,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": False,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        426375,
                    ],
                    "recency_exclusion_window_in_minutes": 306126,
                    "target_trackable_users_enabled": False,
                    "use_mc_id_as_primary": False,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 4735.88,
                    "ctr_in_percent": 9915.94,
                    "nielsen_otp_in_percent": 4475.13,
                    "cpa_in_advertiser_currency": 5150.66,
                    "return_on_ad_spend_percent": 7248.87,
                    "vcr_in_percent": 9972.42,
                    "viewability_in_percent": 6545.2,
                    "vcpm_in_advertiser_currency": 7746.63,
                    "cpcv_in_advertiser_currency": 6813.67,
                    "miaozhen_otp_in_percent": 9625.35,
                },
                "creative_ids": [
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 87.86,
                            "budget_in_impressions": 992162,
                            "daily_target_in_advertiser_currency": 6912.82,
                            "daily_target_in_impressions": 856665,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 2102.57,
                            "budget_in_impressions": 784309,
                            "daily_target_in_advertiser_currency": 9390.93,
                            "daily_target_in_impressions": 704061,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 6477.52,
                            "budget_in_impressions": 511670,
                            "daily_target_in_advertiser_currency": 4530.79,
                            "daily_target_in_impressions": 275977,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": True,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 610092,
                        "demographic_member_ids": [
                            909366,
                            209538,
                        ],
                        "mobile_demographic_member_ids": [
                            493315,
                            778851,
                            468734,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": True,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                        "gender": ttd_workflows.TargetingGender.MALE,
                        "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                        "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                        "countries": [
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 637441,
                            "frequency_goal": 855423,
                            "reset_interval_in_minutes": 967917,
                        },
                    ],
                },
            },
        ],
        "validation_only": False,
    },
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import BackoffStrategy, RetryConfig, parse_datetime


with Workflows(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.campaign.create(request={
        "campaign_create_workflow_primary_input": {
            "advertiser_id": "<id>",
            "name": "<value>",
            "description": "yuck vice between gee ugh ha",
            "time_zone": "Pacific/Chuuk",
            "custom_cpa_click_weight": 7804.86,
            "custom_cpa_viewthrough_weight": 7602.59,
            "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
            "impressions_only_budgeting_cpm": 4492.21,
            "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
            "budget": {
                "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                "budget_in_advertiser_currency": 934.7,
                "budget_in_impressions": 491427,
                "daily_target_in_advertiser_currency": 4904.2,
                "daily_target_in_impressions": 325463,
            },
            "primary_goal": {
                "maximize_reach": False,
                "maximize_ltv_incremental_reach": True,
                "cpc_in_advertiser_currency": 1296.63,
                "ctr_in_percent": 2881.04,
                "nielsen_otp_in_percent": 5833.53,
                "cpa_in_advertiser_currency": 5193.59,
                "return_on_ad_spend_percent": 3259.9,
                "vcr_in_percent": 4078.33,
                "viewability_in_percent": 1012.51,
                "vcpm_in_advertiser_currency": 1884.35,
                "cpcv_in_advertiser_currency": 8133.97,
                "miaozhen_otp_in_percent": 8891.64,
            },
            "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
            "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
            "seed_id": "<id>",
            "campaign_conversion_reporting_columns": [
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 17207,
                    "roas_config": {
                        "include_in_custom_roas": True,
                        "custom_roas_weight": 8441.62,
                        "custom_roas_click_weight": 3535.31,
                        "custom_roas_viewthrough_weight": 4287.45,
                    },
                    "weight": 6798.85,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": True,
                    "reporting_column_id": 860420,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 5665.12,
                        "custom_roas_click_weight": 2955.58,
                        "custom_roas_viewthrough_weight": 2032.57,
                    },
                    "weight": 4332.24,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 995852,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 2127.75,
                        "custom_roas_click_weight": 6207.47,
                        "custom_roas_viewthrough_weight": 2841.2,
                    },
                    "weight": 6083.84,
                    "cross_device_attribution_model_id": "<id>",
                },
            ],
        },
        "campaign_create_advanced_input": {
            "flights": [
                {
                    "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                    "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                    "budget_in_advertiser_currency": 5200.49,
                    "budget_in_impressions": 728836,
                    "daily_target_in_advertiser_currency": 8007.59,
                    "daily_target_in_impressions": 117747,
                },
            ],
            "purchase_order_number": "<value>",
        },
        "ad_groups": [
            {
                "name": "<value>",
                "is_enabled": False,
                "description": "simple ouch when pfft ah",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 6290.63,
                    "budget_in_impressions": 784768,
                    "daily_target_in_advertiser_currency": 3385.24,
                    "daily_target_in_impressions": 913221,
                },
                "base_bid_cpm_in_advertiser_currency": 1541.5,
                "max_bid_cpm_in_advertiser_currency": 7218.8,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": False,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        257762,
                    ],
                    "recency_exclusion_window_in_minutes": 982866,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 3831.56,
                    "ctr_in_percent": 5720.12,
                    "nielsen_otp_in_percent": 9789.08,
                    "cpa_in_advertiser_currency": 1850.76,
                    "return_on_ad_spend_percent": 6168.92,
                    "vcr_in_percent": 9775.91,
                    "viewability_in_percent": 1909.73,
                    "vcpm_in_advertiser_currency": 3141.79,
                    "cpcv_in_advertiser_currency": 8272.61,
                    "miaozhen_otp_in_percent": 7609.47,
                },
                "creative_ids": [
                    "<value>",
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": False,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                            "budget_in_advertiser_currency": 4285.01,
                            "budget_in_impressions": 838181,
                            "daily_target_in_advertiser_currency": 9525.44,
                            "daily_target_in_impressions": 188907,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 8833.21,
                            "budget_in_impressions": 892770,
                            "daily_target_in_advertiser_currency": 1993.11,
                            "daily_target_in_impressions": 564854,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 7458.53,
                            "budget_in_impressions": 290123,
                            "daily_target_in_advertiser_currency": 700.72,
                            "daily_target_in_impressions": 547483,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": False,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 695413,
                        "demographic_member_ids": [
                            261757,
                        ],
                        "mobile_demographic_member_ids": [
                            400422,
                            257433,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [],
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": False,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                        "gender": ttd_workflows.TargetingGender.BOTH,
                        "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                        "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                        "countries": [
                            "<value>",
                            "<value>",
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 557925,
                            "frequency_goal": 643654,
                            "reset_interval_in_minutes": 700013,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 770948,
                            "frequency_goal": 347880,
                            "reset_interval_in_minutes": 698997,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 620608,
                            "frequency_goal": 546216,
                            "reset_interval_in_minutes": 500290,
                        },
                    ],
                },
            },
            {
                "name": "<value>",
                "is_enabled": True,
                "description": "satisfy majority pace however crocodile yowza",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.FIXED,
                    "budget_in_advertiser_currency": 2032.81,
                    "budget_in_impressions": 778234,
                    "daily_target_in_advertiser_currency": 4040.62,
                    "daily_target_in_impressions": 421607,
                },
                "base_bid_cpm_in_advertiser_currency": 9476.87,
                "max_bid_cpm_in_advertiser_currency": 703.96,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": False,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        426375,
                    ],
                    "recency_exclusion_window_in_minutes": 306126,
                    "target_trackable_users_enabled": False,
                    "use_mc_id_as_primary": False,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 4735.88,
                    "ctr_in_percent": 9915.94,
                    "nielsen_otp_in_percent": 4475.13,
                    "cpa_in_advertiser_currency": 5150.66,
                    "return_on_ad_spend_percent": 7248.87,
                    "vcr_in_percent": 9972.42,
                    "viewability_in_percent": 6545.2,
                    "vcpm_in_advertiser_currency": 7746.63,
                    "cpcv_in_advertiser_currency": 6813.67,
                    "miaozhen_otp_in_percent": 9625.35,
                },
                "creative_ids": [
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 87.86,
                            "budget_in_impressions": 992162,
                            "daily_target_in_advertiser_currency": 6912.82,
                            "daily_target_in_impressions": 856665,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 2102.57,
                            "budget_in_impressions": 784309,
                            "daily_target_in_advertiser_currency": 9390.93,
                            "daily_target_in_impressions": 704061,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 6477.52,
                            "budget_in_impressions": 511670,
                            "daily_target_in_advertiser_currency": 4530.79,
                            "daily_target_in_impressions": 275977,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": True,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 610092,
                        "demographic_member_ids": [
                            909366,
                            209538,
                        ],
                        "mobile_demographic_member_ids": [
                            493315,
                            778851,
                            468734,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": True,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                        "gender": ttd_workflows.TargetingGender.MALE,
                        "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                        "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                        "countries": [
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 637441,
                            "frequency_goal": 855423,
                            "reset_interval_in_minutes": 967917,
                        },
                    ],
                },
            },
        ],
        "validation_only": False,
    })

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `create_async` method may raise the following exceptions:

| Error Type                 | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| models.ProblemDetailsError | 400         | application/json |
| models.APIError            | 4XX, 5XX    | \*/\*            |

### Example

```python
import os
import ttd_workflows
from ttd_workflows import Workflows, models
from ttd_workflows.utils import parse_datetime


with Workflows(
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:
    res = None
    try:

        res = workflows.campaign.create(request={
            "campaign_create_workflow_primary_input": {
                "advertiser_id": "<id>",
                "name": "<value>",
                "description": "yuck vice between gee ugh ha",
                "time_zone": "Pacific/Chuuk",
                "custom_cpa_click_weight": 7804.86,
                "custom_cpa_viewthrough_weight": 7602.59,
                "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
                "impressions_only_budgeting_cpm": 4492.21,
                "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
                "budget": {
                    "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                    "budget_in_advertiser_currency": 934.7,
                    "budget_in_impressions": 491427,
                    "daily_target_in_advertiser_currency": 4904.2,
                    "daily_target_in_impressions": 325463,
                },
                "primary_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 1296.63,
                    "ctr_in_percent": 2881.04,
                    "nielsen_otp_in_percent": 5833.53,
                    "cpa_in_advertiser_currency": 5193.59,
                    "return_on_ad_spend_percent": 3259.9,
                    "vcr_in_percent": 4078.33,
                    "viewability_in_percent": 1012.51,
                    "vcpm_in_advertiser_currency": 1884.35,
                    "cpcv_in_advertiser_currency": 8133.97,
                    "miaozhen_otp_in_percent": 8891.64,
                },
                "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
                "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
                "seed_id": "<id>",
                "campaign_conversion_reporting_columns": [
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": False,
                        "reporting_column_id": 17207,
                        "roas_config": {
                            "include_in_custom_roas": True,
                            "custom_roas_weight": 8441.62,
                            "custom_roas_click_weight": 3535.31,
                            "custom_roas_viewthrough_weight": 4287.45,
                        },
                        "weight": 6798.85,
                        "cross_device_attribution_model_id": "<id>",
                    },
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": True,
                        "reporting_column_id": 860420,
                        "roas_config": {
                            "include_in_custom_roas": False,
                            "custom_roas_weight": 5665.12,
                            "custom_roas_click_weight": 2955.58,
                            "custom_roas_viewthrough_weight": 2032.57,
                        },
                        "weight": 4332.24,
                        "cross_device_attribution_model_id": "<id>",
                    },
                    {
                        "tracking_tag_id": "<id>",
                        "include_in_custom_cpa": False,
                        "reporting_column_id": 995852,
                        "roas_config": {
                            "include_in_custom_roas": False,
                            "custom_roas_weight": 2127.75,
                            "custom_roas_click_weight": 6207.47,
                            "custom_roas_viewthrough_weight": 2841.2,
                        },
                        "weight": 6083.84,
                        "cross_device_attribution_model_id": "<id>",
                    },
                ],
            },
            "campaign_create_advanced_input": {
                "flights": [
                    {
                        "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                        "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                        "budget_in_advertiser_currency": 5200.49,
                        "budget_in_impressions": 728836,
                        "daily_target_in_advertiser_currency": 8007.59,
                        "daily_target_in_impressions": 117747,
                    },
                ],
                "purchase_order_number": "<value>",
            },
            "ad_groups": [
                {
                    "name": "<value>",
                    "is_enabled": False,
                    "description": "simple ouch when pfft ah",
                    "programmatic_guaranteed_private_contract_id": "<id>",
                    "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                    "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                    "budget": {
                        "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                        "budget_in_advertiser_currency": 6290.63,
                        "budget_in_impressions": 784768,
                        "daily_target_in_advertiser_currency": 3385.24,
                        "daily_target_in_impressions": 913221,
                    },
                    "base_bid_cpm_in_advertiser_currency": 1541.5,
                    "max_bid_cpm_in_advertiser_currency": 7218.8,
                    "audience_targeting": {
                        "audience_id": "<id>",
                        "audience_accelerator_exclusions_enabled": False,
                        "audience_booster_enabled": False,
                        "audience_excluder_enabled": True,
                        "audience_predictor_enabled": False,
                        "cross_device_vendor_list_for_audience": [
                            257762,
                        ],
                        "recency_exclusion_window_in_minutes": 982866,
                        "target_trackable_users_enabled": True,
                        "use_mc_id_as_primary": True,
                    },
                    "roi_goal": {
                        "maximize_reach": False,
                        "maximize_ltv_incremental_reach": True,
                        "cpc_in_advertiser_currency": 3831.56,
                        "ctr_in_percent": 5720.12,
                        "nielsen_otp_in_percent": 9789.08,
                        "cpa_in_advertiser_currency": 1850.76,
                        "return_on_ad_spend_percent": 6168.92,
                        "vcr_in_percent": 9775.91,
                        "viewability_in_percent": 1909.73,
                        "vcpm_in_advertiser_currency": 3141.79,
                        "cpcv_in_advertiser_currency": 8272.61,
                        "miaozhen_otp_in_percent": 7609.47,
                    },
                    "creative_ids": [
                        "<value>",
                        "<value>",
                    ],
                    "associated_bid_lists": [
                        {
                            "bid_list_id": "<id>",
                            "is_enabled": False,
                            "is_default_for_dimension": False,
                        },
                    ],
                    "advanced_settings": {
                        "flights": [
                            {
                                "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                                "budget_in_advertiser_currency": 4285.01,
                                "budget_in_impressions": 838181,
                                "daily_target_in_advertiser_currency": 9525.44,
                                "daily_target_in_impressions": 188907,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.FIXED,
                                "budget_in_advertiser_currency": 8833.21,
                                "budget_in_impressions": 892770,
                                "daily_target_in_advertiser_currency": 1993.11,
                                "daily_target_in_impressions": 564854,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 7458.53,
                                "budget_in_impressions": 290123,
                                "daily_target_in_advertiser_currency": 700.72,
                                "daily_target_in_impressions": 547483,
                            },
                        ],
                        "koa_optimization_settings": {
                            "are_future_koa_features_enabled": False,
                            "predictive_clearing_enabled": False,
                        },
                        "comscore_settings": {
                            "is_enabled": True,
                            "population_id": 695413,
                            "demographic_member_ids": [
                                261757,
                            ],
                            "mobile_demographic_member_ids": [
                                400422,
                                257433,
                            ],
                        },
                        "contract_targeting": {
                            "allow_open_market_bidding_when_targeting_contracts": True,
                        },
                        "dimensional_bidding_auto_optimization_settings": [
                            [],
                            [
                                ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                            ],
                        ],
                        "is_use_clicks_as_conversions_enabled": False,
                        "is_use_secondary_conversions_enabled": True,
                        "nielsen_tracking_attributes": {
                            "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                            "gender": ttd_workflows.TargetingGender.BOTH,
                            "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                            "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                            "countries": [
                                "<value>",
                                "<value>",
                                "<value>",
                            ],
                        },
                        "new_frequency_configs": [
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 557925,
                                "frequency_goal": 643654,
                                "reset_interval_in_minutes": 700013,
                            },
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 770948,
                                "frequency_goal": 347880,
                                "reset_interval_in_minutes": 698997,
                            },
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 620608,
                                "frequency_goal": 546216,
                                "reset_interval_in_minutes": 500290,
                            },
                        ],
                    },
                },
                {
                    "name": "<value>",
                    "is_enabled": True,
                    "description": "satisfy majority pace however crocodile yowza",
                    "programmatic_guaranteed_private_contract_id": "<id>",
                    "channel": ttd_workflows.AdGroupChannel.VIDEO,
                    "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                    "budget": {
                        "allocation_type": ttd_workflows.AllocationType.FIXED,
                        "budget_in_advertiser_currency": 2032.81,
                        "budget_in_impressions": 778234,
                        "daily_target_in_advertiser_currency": 4040.62,
                        "daily_target_in_impressions": 421607,
                    },
                    "base_bid_cpm_in_advertiser_currency": 9476.87,
                    "max_bid_cpm_in_advertiser_currency": 703.96,
                    "audience_targeting": {
                        "audience_id": "<id>",
                        "audience_accelerator_exclusions_enabled": True,
                        "audience_booster_enabled": False,
                        "audience_excluder_enabled": False,
                        "audience_predictor_enabled": False,
                        "cross_device_vendor_list_for_audience": [
                            426375,
                        ],
                        "recency_exclusion_window_in_minutes": 306126,
                        "target_trackable_users_enabled": False,
                        "use_mc_id_as_primary": False,
                    },
                    "roi_goal": {
                        "maximize_reach": False,
                        "maximize_ltv_incremental_reach": True,
                        "cpc_in_advertiser_currency": 4735.88,
                        "ctr_in_percent": 9915.94,
                        "nielsen_otp_in_percent": 4475.13,
                        "cpa_in_advertiser_currency": 5150.66,
                        "return_on_ad_spend_percent": 7248.87,
                        "vcr_in_percent": 9972.42,
                        "viewability_in_percent": 6545.2,
                        "vcpm_in_advertiser_currency": 7746.63,
                        "cpcv_in_advertiser_currency": 6813.67,
                        "miaozhen_otp_in_percent": 9625.35,
                    },
                    "creative_ids": [
                        "<value>",
                    ],
                    "associated_bid_lists": [
                        {
                            "bid_list_id": "<id>",
                            "is_enabled": False,
                            "is_default_for_dimension": True,
                        },
                    ],
                    "advanced_settings": {
                        "flights": [
                            {
                                "allocation_type": ttd_workflows.AllocationType.FIXED,
                                "budget_in_advertiser_currency": 87.86,
                                "budget_in_impressions": 992162,
                                "daily_target_in_advertiser_currency": 6912.82,
                                "daily_target_in_impressions": 856665,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 2102.57,
                                "budget_in_impressions": 784309,
                                "daily_target_in_advertiser_currency": 9390.93,
                                "daily_target_in_impressions": 704061,
                            },
                            {
                                "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                                "budget_in_advertiser_currency": 6477.52,
                                "budget_in_impressions": 511670,
                                "daily_target_in_advertiser_currency": 4530.79,
                                "daily_target_in_impressions": 275977,
                            },
                        ],
                        "koa_optimization_settings": {
                            "are_future_koa_features_enabled": False,
                            "predictive_clearing_enabled": True,
                        },
                        "comscore_settings": {
                            "is_enabled": True,
                            "population_id": 610092,
                            "demographic_member_ids": [
                                909366,
                                209538,
                            ],
                            "mobile_demographic_member_ids": [
                                493315,
                                778851,
                                468734,
                            ],
                        },
                        "contract_targeting": {
                            "allow_open_market_bidding_when_targeting_contracts": True,
                        },
                        "dimensional_bidding_auto_optimization_settings": [
                            [
                                ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                            ],
                        ],
                        "is_use_clicks_as_conversions_enabled": True,
                        "is_use_secondary_conversions_enabled": True,
                        "nielsen_tracking_attributes": {
                            "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                            "gender": ttd_workflows.TargetingGender.MALE,
                            "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                            "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                            "countries": [
                                "<value>",
                            ],
                        },
                        "new_frequency_configs": [
                            {
                                "counter_name": "<value>",
                                "frequency_cap": 637441,
                                "frequency_goal": 855423,
                                "reset_interval_in_minutes": 967917,
                            },
                        ],
                    },
                },
            ],
            "validation_only": False,
        })

        # Handle response
        print(res)

    except models.ProblemDetailsError as e:
        # handle e.data: models.ProblemDetailsErrorData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import os
import ttd_workflows
from ttd_workflows import Workflows
from ttd_workflows.utils import parse_datetime


with Workflows(
    server_url="https://api.thetradedesk.com/workflows",
    ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
) as workflows:

    res = workflows.campaign.create(request={
        "campaign_create_workflow_primary_input": {
            "advertiser_id": "<id>",
            "name": "<value>",
            "description": "yuck vice between gee ugh ha",
            "time_zone": "Pacific/Chuuk",
            "custom_cpa_click_weight": 7804.86,
            "custom_cpa_viewthrough_weight": 7602.59,
            "custom_cpa_type": ttd_workflows.CustomCPAType.DISABLED,
            "impressions_only_budgeting_cpm": 4492.21,
            "primary_channel": ttd_workflows.CampaignChannelType.AUDIO,
            "budget": {
                "pacing_mode": ttd_workflows.CampaignPacingMode.PACE_TO_DAILY_CAP,
                "budget_in_advertiser_currency": 934.7,
                "budget_in_impressions": 491427,
                "daily_target_in_advertiser_currency": 4904.2,
                "daily_target_in_impressions": 325463,
            },
            "primary_goal": {
                "maximize_reach": False,
                "maximize_ltv_incremental_reach": True,
                "cpc_in_advertiser_currency": 1296.63,
                "ctr_in_percent": 2881.04,
                "nielsen_otp_in_percent": 5833.53,
                "cpa_in_advertiser_currency": 5193.59,
                "return_on_ad_spend_percent": 3259.9,
                "vcr_in_percent": 4078.33,
                "viewability_in_percent": 1012.51,
                "vcpm_in_advertiser_currency": 1884.35,
                "cpcv_in_advertiser_currency": 8133.97,
                "miaozhen_otp_in_percent": 8891.64,
            },
            "start_date_in_utc": parse_datetime("2023-01-06T22:59:38.009Z"),
            "end_date_in_utc": parse_datetime("2025-09-26T06:26:29.839Z"),
            "seed_id": "<id>",
            "campaign_conversion_reporting_columns": [
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 17207,
                    "roas_config": {
                        "include_in_custom_roas": True,
                        "custom_roas_weight": 8441.62,
                        "custom_roas_click_weight": 3535.31,
                        "custom_roas_viewthrough_weight": 4287.45,
                    },
                    "weight": 6798.85,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": True,
                    "reporting_column_id": 860420,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 5665.12,
                        "custom_roas_click_weight": 2955.58,
                        "custom_roas_viewthrough_weight": 2032.57,
                    },
                    "weight": 4332.24,
                    "cross_device_attribution_model_id": "<id>",
                },
                {
                    "tracking_tag_id": "<id>",
                    "include_in_custom_cpa": False,
                    "reporting_column_id": 995852,
                    "roas_config": {
                        "include_in_custom_roas": False,
                        "custom_roas_weight": 2127.75,
                        "custom_roas_click_weight": 6207.47,
                        "custom_roas_viewthrough_weight": 2841.2,
                    },
                    "weight": 6083.84,
                    "cross_device_attribution_model_id": "<id>",
                },
            ],
        },
        "campaign_create_advanced_input": {
            "flights": [
                {
                    "start_date_inclusive_utc": parse_datetime("2024-06-28T18:56:13.043Z"),
                    "end_date_exclusive_utc": parse_datetime("2024-10-30T06:59:44.964Z"),
                    "budget_in_advertiser_currency": 5200.49,
                    "budget_in_impressions": 728836,
                    "daily_target_in_advertiser_currency": 8007.59,
                    "daily_target_in_impressions": 117747,
                },
            ],
            "purchase_order_number": "<value>",
        },
        "ad_groups": [
            {
                "name": "<value>",
                "is_enabled": False,
                "description": "simple ouch when pfft ah",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.NATIVE_VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                    "budget_in_advertiser_currency": 6290.63,
                    "budget_in_impressions": 784768,
                    "daily_target_in_advertiser_currency": 3385.24,
                    "daily_target_in_impressions": 913221,
                },
                "base_bid_cpm_in_advertiser_currency": 1541.5,
                "max_bid_cpm_in_advertiser_currency": 7218.8,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": False,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": True,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        257762,
                    ],
                    "recency_exclusion_window_in_minutes": 982866,
                    "target_trackable_users_enabled": True,
                    "use_mc_id_as_primary": True,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 3831.56,
                    "ctr_in_percent": 5720.12,
                    "nielsen_otp_in_percent": 9789.08,
                    "cpa_in_advertiser_currency": 1850.76,
                    "return_on_ad_spend_percent": 6168.92,
                    "vcr_in_percent": 9775.91,
                    "viewability_in_percent": 1909.73,
                    "vcpm_in_advertiser_currency": 3141.79,
                    "cpcv_in_advertiser_currency": 8272.61,
                    "miaozhen_otp_in_percent": 7609.47,
                },
                "creative_ids": [
                    "<value>",
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": False,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.MINIMUM,
                            "budget_in_advertiser_currency": 4285.01,
                            "budget_in_impressions": 838181,
                            "daily_target_in_advertiser_currency": 9525.44,
                            "daily_target_in_impressions": 188907,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 8833.21,
                            "budget_in_impressions": 892770,
                            "daily_target_in_advertiser_currency": 1993.11,
                            "daily_target_in_impressions": 564854,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 7458.53,
                            "budget_in_impressions": 290123,
                            "daily_target_in_advertiser_currency": 700.72,
                            "daily_target_in_impressions": 547483,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": False,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 695413,
                        "demographic_member_ids": [
                            261757,
                        ],
                        "mobile_demographic_member_ids": [
                            400422,
                            257433,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [],
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_VIDEO_COMPLETION_RATE_SCORE_RANGE,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": False,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.AUDIENCE,
                        "gender": ttd_workflows.TargetingGender.BOTH,
                        "start_age": ttd_workflows.TargetingStartAge.TWENTY_FIVE,
                        "end_age": ttd_workflows.TargetingEndAge.TWENTY_NINE,
                        "countries": [
                            "<value>",
                            "<value>",
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 557925,
                            "frequency_goal": 643654,
                            "reset_interval_in_minutes": 700013,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 770948,
                            "frequency_goal": 347880,
                            "reset_interval_in_minutes": 698997,
                        },
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 620608,
                            "frequency_goal": 546216,
                            "reset_interval_in_minutes": 500290,
                        },
                    ],
                },
            },
            {
                "name": "<value>",
                "is_enabled": True,
                "description": "satisfy majority pace however crocodile yowza",
                "programmatic_guaranteed_private_contract_id": "<id>",
                "channel": ttd_workflows.AdGroupChannel.VIDEO,
                "funnel_location": ttd_workflows.AdGroupFunnelLocation.NONE,
                "budget": {
                    "allocation_type": ttd_workflows.AllocationType.FIXED,
                    "budget_in_advertiser_currency": 2032.81,
                    "budget_in_impressions": 778234,
                    "daily_target_in_advertiser_currency": 4040.62,
                    "daily_target_in_impressions": 421607,
                },
                "base_bid_cpm_in_advertiser_currency": 9476.87,
                "max_bid_cpm_in_advertiser_currency": 703.96,
                "audience_targeting": {
                    "audience_id": "<id>",
                    "audience_accelerator_exclusions_enabled": True,
                    "audience_booster_enabled": False,
                    "audience_excluder_enabled": False,
                    "audience_predictor_enabled": False,
                    "cross_device_vendor_list_for_audience": [
                        426375,
                    ],
                    "recency_exclusion_window_in_minutes": 306126,
                    "target_trackable_users_enabled": False,
                    "use_mc_id_as_primary": False,
                },
                "roi_goal": {
                    "maximize_reach": False,
                    "maximize_ltv_incremental_reach": True,
                    "cpc_in_advertiser_currency": 4735.88,
                    "ctr_in_percent": 9915.94,
                    "nielsen_otp_in_percent": 4475.13,
                    "cpa_in_advertiser_currency": 5150.66,
                    "return_on_ad_spend_percent": 7248.87,
                    "vcr_in_percent": 9972.42,
                    "viewability_in_percent": 6545.2,
                    "vcpm_in_advertiser_currency": 7746.63,
                    "cpcv_in_advertiser_currency": 6813.67,
                    "miaozhen_otp_in_percent": 9625.35,
                },
                "creative_ids": [
                    "<value>",
                ],
                "associated_bid_lists": [
                    {
                        "bid_list_id": "<id>",
                        "is_enabled": False,
                        "is_default_for_dimension": True,
                    },
                ],
                "advanced_settings": {
                    "flights": [
                        {
                            "allocation_type": ttd_workflows.AllocationType.FIXED,
                            "budget_in_advertiser_currency": 87.86,
                            "budget_in_impressions": 992162,
                            "daily_target_in_advertiser_currency": 6912.82,
                            "daily_target_in_impressions": 856665,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 2102.57,
                            "budget_in_impressions": 784309,
                            "daily_target_in_advertiser_currency": 9390.93,
                            "daily_target_in_impressions": 704061,
                        },
                        {
                            "allocation_type": ttd_workflows.AllocationType.MAXIMUM,
                            "budget_in_advertiser_currency": 6477.52,
                            "budget_in_impressions": 511670,
                            "daily_target_in_advertiser_currency": 4530.79,
                            "daily_target_in_impressions": 275977,
                        },
                    ],
                    "koa_optimization_settings": {
                        "are_future_koa_features_enabled": False,
                        "predictive_clearing_enabled": True,
                    },
                    "comscore_settings": {
                        "is_enabled": True,
                        "population_id": 610092,
                        "demographic_member_ids": [
                            909366,
                            209538,
                        ],
                        "mobile_demographic_member_ids": [
                            493315,
                            778851,
                            468734,
                        ],
                    },
                    "contract_targeting": {
                        "allow_open_market_bidding_when_targeting_contracts": True,
                    },
                    "dimensional_bidding_auto_optimization_settings": [
                        [
                            ttd_workflows.DimensionalBiddingDimensions.HAS_INTEGRAL_VIDEO_BRAND_SAFETY_CATEGORY_ID,
                        ],
                    ],
                    "is_use_clicks_as_conversions_enabled": True,
                    "is_use_secondary_conversions_enabled": True,
                    "nielsen_tracking_attributes": {
                        "enhanced_reporting_option": ttd_workflows.EnhancedNielsenReportingOptions.SITE,
                        "gender": ttd_workflows.TargetingGender.MALE,
                        "start_age": ttd_workflows.TargetingStartAge.EIGHTEEN,
                        "end_age": ttd_workflows.TargetingEndAge.FORTY_FOUR,
                        "countries": [
                            "<value>",
                        ],
                    },
                    "new_frequency_configs": [
                        {
                            "counter_name": "<value>",
                            "frequency_cap": 637441,
                            "frequency_goal": 855423,
                            "reset_interval_in_minutes": 967917,
                        },
                    ],
                },
            },
        ],
        "validation_only": False,
    })

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from ttd_workflows import Workflows
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Workflows(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from ttd_workflows import Workflows
from ttd_workflows.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Workflows(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Workflows` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
import os
from ttd_workflows import Workflows
def main():

    with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Workflows(
        ttd_auth=os.getenv("WORKFLOWS_TTD_AUTH", ""),
    ) as workflows:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from ttd_workflows import Workflows
import logging

logging.basicConfig(level=logging.DEBUG)
s = Workflows(debug_logger=logging.getLogger("ttd_workflows"))
```

You can also enable a default debug logger by setting an environment variable `WORKFLOWS_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
