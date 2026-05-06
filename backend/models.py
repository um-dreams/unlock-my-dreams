import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    auth_provider = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user", uselist=False)
    business_plans = relationship("BusinessPlan", back_populates="user")
    websites = relationship("Website", back_populates="user")
    llc_registrations = relationship("LLCRegistration", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tier = Column(String, default="free") # free, pro, business
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    status = Column(String, default="active") # active, canceled, past_due
    current_period_end = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="subscriptions")

class BusinessPlan(Base):
    __tablename__ = "business_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    idea_description = Column(Text)
    plan_content = Column(JSONB)
    status = Column(String, default="draft") # draft, complete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="business_plans")
    checklist = relationship("Checklist", back_populates="business_plan", uselist=False)
    websites = relationship("Website", back_populates="business_plan")
    llc_registration = relationship("LLCRegistration", back_populates="business_plan", uselist=False)

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_plan_id = Column(UUID(as_uuid=True), ForeignKey("business_plans.id"))
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    business_plan = relationship("BusinessPlan", back_populates="checklist")
    items = relationship("ChecklistItem", back_populates="checklist")

class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checklist_id = Column(UUID(as_uuid=True), ForeignKey("checklists.id"))
    title = Column(String)
    description = Column(Text)
    sort_order = Column(Integer)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    checklist = relationship("Checklist", back_populates="items")

class Website(Base):
    __tablename__ = "websites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    business_plan_id = Column(UUID(as_uuid=True), ForeignKey("business_plans.id"))
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"))
    name = Column(String)
    subdomain = Column(String, unique=True, nullable=True)
    status = Column(String, default="draft") # draft, published
    published_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="websites")
    business_plan = relationship("BusinessPlan", back_populates="websites")
    template = relationship("Template")
    pages = relationship("Page", back_populates="website")
    domain = relationship("Domain", back_populates="website", uselist=False)

class Page(Base):
    __tablename__ = "pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    website_id = Column(UUID(as_uuid=True), ForeignKey("websites.id"))
    title = Column(String)
    slug = Column(String)
    page_type = Column(String) # landing, about, services, blog, store
    content = Column(JSONB)
    sort_order = Column(Integer)

    website = relationship("Website", back_populates="pages")

class Template(Base):
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    category = Column(String)
    layout_config = Column(JSONB)
    is_premium = Column(Boolean, default=False)

class Domain(Base):
    __tablename__ = "domains"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    website_id = Column(UUID(as_uuid=True), ForeignKey("websites.id"))
    domain_name = Column(String, unique=True)
    verification_status = Column(String, default="pending") # pending, verified, failed
    dns_records = Column(JSONB, nullable=True)

    website = relationship("Website", back_populates="domain")

class LLCRegistration(Base):
    __tablename__ = "llc_registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    business_plan_id = Column(UUID(as_uuid=True), ForeignKey("business_plans.id"))
    state = Column(String)
    entity_name = Column(String)
    status = Column(String, default="draft") # draft, submitted, approved, rejected
    partner_reference_id = Column(String, nullable=True)
    filing_fee = Column(Numeric(10, 2), nullable=True)
    filed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="llc_registrations")
    business_plan = relationship("BusinessPlan", back_populates="llc_registration")
    documents = relationship("Document", back_populates="llc_registration")
    compliance_events = relationship("ComplianceEvent", back_populates="llc_registration")

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    llc_registration_id = Column(UUID(as_uuid=True), ForeignKey("llc_registrations.id"))
    doc_type = Column(String) # operating_agreement, ein_application, articles
    s3_key = Column(String)
    status = Column(String, default="draft") # draft, final
    generated_at = Column(DateTime, default=datetime.utcnow)

    llc_registration = relationship("LLCRegistration", back_populates="documents")

class ComplianceEvent(Base):
    __tablename__ = "compliance_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    llc_registration_id = Column(UUID(as_uuid=True), ForeignKey("llc_registrations.id"))
    event_type = Column(String) # annual_report, franchise_tax, agent_renewal
    title = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)

    llc_registration = relationship("LLCRegistration", back_populates="compliance_events")
