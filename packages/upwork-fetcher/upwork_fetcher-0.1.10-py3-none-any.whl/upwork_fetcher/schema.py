from typing import Any, Dict, Optional, List, TypedDict
from pydantic import BaseModel, field_validator


# Define typed dictionaries for nested structures
class SkillDict(TypedDict):
    name: str
    prettyName: str
    highlighted: bool


class AmountDict(TypedDict):
    rawValue: str
    currency: str
    displayValue: str


class LocationDict(TypedDict):
    city: Optional[str]
    country: Optional[str]
    timezone: Optional[str]
    state: Optional[str]
    offsetToUTC: Optional[str]


class ClientDict(TypedDict):
    edcUserId: Optional[str]
    totalHires: Optional[int]
    totalPostedJobs: Optional[int]
    location: Optional[LocationDict]
    totalSpent: Optional[Dict[str, float]]
    totalReviews: Optional[int]
    totalFeedback: Optional[float]
    companyRid: Optional[str]
    companyName: Optional[str]
    lastContractPlatform: Optional[str]
    lastContractRid: Optional[str]
    lastContractTitle: Optional[str]
    hasFinancialPrivacy: Optional[bool]


class JobSchema(BaseModel):
    id: str
    title: str
    description: str
    category: str
    total_applicants: int
    preferred_freelancer_location: Optional[str]
    preferred_freelancer_location_mandatory: bool
    premium: bool
    experience_level: str
    amount_raw_value: str
    amount_currency: str
    amount_display_value: str
    skills: List[SkillDict]
    hourly_budget_type: Optional[str]
    hourly_budget_min: Optional[float]
    hourly_budget_max: Optional[float]
    duration: Optional[str]
    client_not_sure_fields: Optional[str]
    client_private_fields: Optional[str]
    freelancer_client_relation: Optional[str]
    local_job_user_distance: Optional[str]
    weekly_budget_raw_value: Optional[str]
    weekly_budget_currency: Optional[str]
    weekly_budget_display_value: Optional[str]
    engagement_duration_id: Optional[str]
    engagement_duration_label: Optional[str]
    engagement_duration_weeks: Optional[int]
    client_edc_user_id: Optional[str]
    client_total_hires: Optional[int]
    client_total_posted_jobs: Optional[int]
    client_total_spent: Optional[float]
    client_location_city: Optional[str]
    client_location_country: Optional[str]
    client_location_timezone: Optional[str]
    client_location_state: Optional[str]
    client_location_offset_to_utc: Optional[str]
    client_total_reviews: Optional[int]
    client_total_feedback: Optional[float]
    client_company_rid: Optional[str]
    client_company_name: Optional[str]
    client_last_contract_platform: Optional[str]
    client_last_contract_rid: Optional[str]
    client_last_contract_title: Optional[str]
    client_has_financial_privacy: Optional[bool]
    occupations_category_id: Optional[str]
    occupations_category_pref_label: Optional[str]
    created_date_time: Optional[str]  # Consider using datetime
    published_date_time: Optional[str]  # Consider using datetime

    @classmethod
    def create_instance(cls, data: Dict[str, Any]) -> "JobSchema":
        # Safely get nested dictionary values
        amount: Dict[str, Any] = data.get("amount") or {}
        weekly_budget: Dict[str, Any] = data.get("weeklyBudget") or {}
        engagement_duration: Dict[str, Any] = data.get("engagementDuration") or {}
        client: ClientDict = data.get("client", {})
        client_location: Optional[LocationDict] = client.get("location")
        client_total_spent: Dict[str, Any] = client.get("totalSpent") or {}
        occupations_category: Dict[str, Any] = data.get("occupationsCategory", {}) or {}
        hourly_budget_min: Dict[str, Any] = data.get("hourlyBudgetMin") or {}
        hourly_budget_max: Dict[str, Any] = data.get("hourlyBudgetMax") or {}

        return cls(
            id=data.get("id", ""),  # singleLineText
            title=data.get("title", ""),  # singleLineText
            description=data.get("description", ""),
            category=data.get("category", ""),  # singleLineText
            total_applicants=data.get("totalApplicants", 0),  # number
            preferred_freelancer_location=data.get(
                "preferredFreelancerLocation"
            ),  # singleLineText
            preferred_freelancer_location_mandatory=data.get(
                "preferredFreelancerLocationMandatory", ""
            ),  # checkbox
            premium=data.get("premium", False),  # checkbox
            experience_level=data.get("experienceLevel", ""),  # singleLineText
            amount_raw_value=amount.get("rawValue", 0),  # number
            amount_currency=amount.get("currency", ""),  # singleLineText
            amount_display_value=amount.get("displayValue", ""),  # singleLineText
            skills=data.get("skills", []),  # multipleSelects
            hourly_budget_type=data.get("hourlyBudgetType"),  # singleLineText
            hourly_budget_min=hourly_budget_min.get("rawValue"),  # number
            hourly_budget_max=hourly_budget_max.get("rawValue"),  # number
            duration=data.get("duration"),  # singleLineText
            client_not_sure_fields=data.get("clientNotSureFields"),  # singleLineText
            client_private_fields=data.get("clientPrivateFields"),  # singleLineText
            freelancer_client_relation=data.get(
                "freelancerClientRelation"
            ),  # singleLineText
            local_job_user_distance=data.get("localJobUserDistance"),  # singleLineText
            weekly_budget_raw_value=weekly_budget.get("rawValue"),  # number
            weekly_budget_currency=weekly_budget.get("currency"),  # singleLineText
            weekly_budget_display_value=weekly_budget.get(
                "displayValue"
            ),  # singleLineText
            engagement_duration_id=engagement_duration.get("id"),  # singleLineText
            engagement_duration_label=engagement_duration.get(
                "label"
            ),  # singleLineText
            engagement_duration_weeks=engagement_duration.get("weeks"),  # number
            client_edc_user_id=client.get("edcUserId"),  # singleLineText
            client_total_hires=client.get("totalHires"),  # number
            client_total_posted_jobs=client.get("totalPostedJobs"),  # number
            client_total_spent=client_total_spent.get("rawValue"),  # number
            client_location_city=(
                client_location.get("city") if client_location else None
            ),  # singleLineText
            client_location_country=(
                client_location.get("country") if client_location else None
            ),  # singleLineText
            client_location_timezone=(
                client_location.get("timezone") if client_location else None
            ),  # singleLineText
            client_location_state=(
                client_location.get("state") if client_location else None
            ),  # singleLineText
            client_location_offset_to_utc=(
                client_location.get("offsetToUTC") if client_location else None
            ),  # singleLineText
            client_total_reviews=client.get("totalReviews"),  # number
            client_total_feedback=client.get("totalFeedback"),  # number
            client_company_rid=client.get("companyRid"),  # singleLineText
            client_company_name=client.get("companyName"),  # singleLineText
            client_last_contract_platform=client.get(
                "lastContractPlatform"
            ),  # singleLineText
            client_last_contract_rid=client.get("lastContractRid"),  # singleLineText
            client_last_contract_title=client.get(
                "lastContractTitle"
            ),  # singleLineText
            client_has_financial_privacy=client.get("hasFinancialPrivacy"),  # checkbox
            occupations_category_id=occupations_category.get("id"),  # singleLineText
            occupations_category_pref_label=occupations_category.get(
                "prefLabel"
            ),  # singleLineText
            created_date_time=data.get("createdDateTime"),  # singleLineText
            published_date_time=data.get("publishedDateTime"),  # singleLineText
        )

    @field_validator("preferred_freelancer_location", mode="before")
    @classmethod
    def preferred_freelancer_location_validator(
        cls, value: List[str] | None
    ) -> str | None:
        if isinstance(value, list):
            return " ".join(value)
        return value

    def __str__(self) -> str:
        return f"Job(id='{self.id}', title='{self.title}')"

    def __repr__(self) -> str:
        return self.__str__()

    class Meta:
        orm_mode = True
