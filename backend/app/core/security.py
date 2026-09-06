"""
RBAC & Clearance Levels for Industrial Users (PSUs/Defense).
Levels:
1 = INTERNAL (Floor Engineers, Contractors)
2 = CONFIDENTIAL (Reliability Officers, Plant Managers)
3 = SECRET (Chief General Managers, Board / Ministry Clearance)
"""
from enum import IntEnum
from typing import Dict, Optional
from pydantic import BaseModel

class ClearanceTier(IntEnum):
    INTERNAL = 1
    CONFIDENTIAL = 2
    SECRET = 3

    @classmethod
    def from_str(cls, label: str) -> "ClearanceTier":
        clean = label.strip().upper()
        if "SEC" in clean:
            return cls.SECRET
        if "CONF" in clean:
            return cls.CONFIDENTIAL
        return cls.INTERNAL

class UserIdentity(BaseModel):
    user_id: str
    name: str
    department: str
    clearance_tier: ClearanceTier
    role: str

# Pre-seeded Mock Enterprise Personas for Hackathon Demos
MOCK_PERSONAS: Dict[str, UserIdentity] = {
    "eng_rahul": UserIdentity(
        user_id="eng_rahul",
        name="Rahul Verma",
        department="Mechanical Maintenance (Unit 2)",
        clearance_tier=ClearanceTier.INTERNAL,
        role="Plant Process Engineer"
    ),
    "officer_priya": UserIdentity(
        user_id="officer_priya",
        name="Priya Nair",
        department="Asset Integrity & Quality Inspection",
        clearance_tier=ClearanceTier.CONFIDENTIAL,
        role="Lead Reliability Inspector"
    ),
    "cgm_sharma": UserIdentity(
        user_id="cgm_sharma",
        name="Dr. V. K. Sharma",
        department="Refinery Operations & Ministry Liaison",
        clearance_tier=ClearanceTier.SECRET,
        role="Chief General Manager (Operations)"
    )
}

def resolve_user(user_id: Optional[str] = None, clearance_override: Optional[int] = None) -> UserIdentity:
    user = MOCK_PERSONAS.get(user_id or "eng_rahul")
    if not user:
        tier = ClearanceTier(clearance_override) if clearance_override in [1, 2, 3] else ClearanceTier.INTERNAL
        return UserIdentity(
            user_id=user_id or "custom_user",
            name="Industrial Operator",
            department="Operations",
            clearance_tier=tier,
            role="On-Premise Operator"
        )
    if clearance_override and clearance_override in [1, 2, 3]:
        # Return cloned user with override for testing
        return UserIdentity(
            user_id=user.user_id,
            name=user.name,
            department=user.department,
            clearance_tier=ClearanceTier(clearance_override),
            role=user.role
        )
    return user
