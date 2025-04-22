from abc import ABC, abstractmethod
from digitaltwins_on_fhir.core.resource import ImagingStudy, Reference


class AbstractSearch(ABC):
    core = None

    def __init__(self, core):
        self.core = core

    @abstractmethod
    def search_resource_async(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resources_async(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resource_sync(self, resource_type, identifier):
        pass

    @abstractmethod
    def search_resources_sync(self, resource_type, identifier):
        pass


class Search(AbstractSearch):
    async_client = None

    def __init__(self, core):
        super().__init__(core)
        self.async_client = self.core.async_client
        self.sync_client = self.core.sync_client

    async def search_resource_async(self, resource_type, identifier):
        resources_search_set = self.async_client.resources(resource_type)
        searched_resource = await resources_search_set.search(identifier=identifier).first()
        return searched_resource

    async def search_resources_async(self, resource_type, identifier=None):
        resources_search_set = self.async_client.resources(resource_type)
        if identifier is None:
            resources = await resources_search_set.search().fetch_all()
        else:
            resources = await resources_search_set.search(identifier=identifier).fetch_all()
        return resources

    def search_resource_sync(self, resource_type, identifier):
        resources_search_set = self.sync_client.resources(resource_type)
        searched_resource = resources_search_set.search(identifier=identifier).first()
        return searched_resource

    def search_resources_sync(self, resource_type, identifier=None):
        resources_search_set = self.sync_client.resources(resource_type)
        if identifier is None:
            resources = resources_search_set.search().fetch_all()
        else:
            resources = resources_search_set.search(identifier=identifier).fetch_all()
        return resources

    async def get_dataset_information(self, dataset_identifier):
        infos = {}

        research_study = await self.search_resource_async("ResearchStudy", dataset_identifier)
        if research_study is None:
            return None
        group_search_set = self.async_client.resources("Group")
        group = await group_search_set.search(
            characteristic_value=research_study.to_reference()).first()
        practitioner = await group["managingEntity"].to_resource()

        infos["dataset"] = research_study
        infos["practitioner"] = practitioner
        infos["group"] = group
        infos["patients"] = []

        for p in group["member"]:
            appointment = await self.async_client.resources("Appointment").search(patient=p.get("entity"),
                                                                                  supporting_info=research_study.to_reference()).first()
            encounter = await self.async_client.resources("Encounter").search(patient=p.get("entity"),
                                                                              appointment=appointment.to_reference()).first()
            count_imaging_study = self.sync_client.resources('ImagingStudy').search(
                encounter=encounter.to_reference()).count()
            count_observation = self.sync_client.resources('Observation').search(
                encounter=encounter.to_reference()).count()

            imagings = await self.async_client.resources("ImagingStudy").search(
                encounter=encounter.to_reference()).limit(count_imaging_study).fetch()

            infos["patients"].append({
                "patient": await p.get("entity").to_resource(),
                "appointment": appointment,
                "encounter": encounter,
                "observations": await self.async_client.resources("Observation").search(
                    encounter=encounter.to_reference()).limit(count_observation).fetch(),
                "imagingstudies": imagings
            })

        return infos

    async def get_patient_measurements(self, patient_identifier, patient_id):
        measurements = {}

        if not isinstance(patient_id, str):
            patient_id = str(patient_id)
        patients = await self.search_resources_async(resource_type="Patient", identifier=patient_identifier)

        if len(patients) == 0:
            return measurements

        for p in patients:
            if p.get("id") == patient_id:
                appointment_count = self.sync_client.resources("Appointment").search(patient=p.get("entity")).count()
                measurements["patient_identifier"] = p.get_by_path(["identifier", 0, "value"])
                appointments = await self.async_client.resources("Appointment").search(patient=p.get("entity")).limit(
                    appointment_count).fetch()
                measurements["appointments"] = []
                for a in appointments:
                    temp_a = {"appointment_identifier": a.get_by_path(["identifier", 0, "value"])}
                    encounter_count = self.sync_client.resources("Encounter").search(patient=p.get("entity"),
                                                                                     appointment=a.to_reference()).count

                    measurements["appointments"].append(temp_a)

        return measurements
