import requests
import robocorp.log


class ERP:
    default_timeout = 90

    @staticmethod
    def get_customers(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = (
                    f"{base_url}/customers?company_id={company_id}&token={login_token}"
                )
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return Customers(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_customer(base_url, company_id, login_token, customer_id):
        try:
            if isinstance(customer_id, list):
                customers = []
                for c_id in customer_id:
                    with robocorp.log.suppress_variables():
                        url = f"{base_url}/customers/{c_id}?company_id={company_id}&token={login_token}"
                        response = requests.get(url, timeout=ERP.default_timeout)
                        response.raise_for_status()
                        customers.append(Customer(response.json()))
                return customers
            else:
                with robocorp.log.suppress_variables():
                    url = f"{base_url}/customers/{customer_id}?company_id={company_id}&token={login_token}"
                    response = requests.get(url, timeout=ERP.default_timeout)
                    response.raise_for_status()
                    return Customer(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_customer_categories(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/customers/categories?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return Categories(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_customer_groups(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/customers/groups?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return Groups(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_employees(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = (
                    f"{base_url}/employees?company_id={company_id}&token={login_token}"
                )
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return Employees(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_employee(base_url, company_id, login_token, employee_id):
        try:
            if isinstance(employee_id, list):
                employees = []
                for e_id in employee_id:
                    with robocorp.log.suppress_variables():
                        url = f"{base_url}/employees/{e_id}?company_id={company_id}&token={login_token}"
                        response = requests.get(url, timeout=ERP.default_timeout)
                        response.raise_for_status()
                        employees.append(Employee(response.json()))
                return employees
            else:
                with robocorp.log.suppress_variables():
                    url = f"{base_url}/employees/{employee_id}?company_id={company_id}&token={login_token}"
                    response = requests.get(url, timeout=ERP.default_timeout)
                    response.raise_for_status()
                    return Employee(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_employee_groups(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/employee/groups?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return EmployeeGroups(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_employee_teams(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/employee/teams?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return EmployeeTeams(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_product_type_categories(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/product_types/categories?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return ProductTypes(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_product_types(base_url, company_id, login_token):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/product_types?company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return ProductTypes(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_product_type(base_url, company_id, login_token, product_type_id):
        try:
            if isinstance(product_type_id, list):
                product_types = []
                for p_id in product_type_id:
                    with robocorp.log.suppress_variables():
                        url = f"{base_url}/product_types/{p_id}?company_id={company_id}&token={login_token}"
                        response = requests.get(url, timeout=ERP.default_timeout)
                        response.raise_for_status()
                        product_types.append(ProductType(response.json()))
                return product_types
            else:
                with robocorp.log.suppress_variables():
                    url = f"{base_url}/product_types/{product_type_id}?company_id={company_id}&token={login_token}"
                    response = requests.get(url, timeout=ERP.default_timeout)
                    response.raise_for_status()
                    return ProductType(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_customer_invoicing_report(
        base_url,
        company_id,
        login_token,
        term_start,
        term_end,
        customer_ids=None,
        employee_ids=None,
        project_template_ids=None,
        project_task_template_ids=None,
        product_type_ids=None,
        sessions_cost=False,
        contract_cost=False,
        services_cost=False,
        products_cost=False,
        internal_cost=False,
        internal_product_cost=False,
    ):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/report/customer_invoicing?selection%5Bterm_start%5D={term_start}&selection%5Bterm_end%5D={term_end}"

                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&selection%5B{param_name}%5D%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return "".join(
                            f"&selection%5B{param_name}%5D%5B%5D={str(id_)}"
                            for id_ in param_value
                        )
                    return ""

                if customer_ids is not None:
                    url += add_ids_to_url("customer_ids", customer_ids)

                if employee_ids is not None:
                    url += add_ids_to_url("employee_ids", employee_ids)

                if project_template_ids is not None:
                    url += add_ids_to_url("project_template_ids", project_template_ids)

                if project_task_template_ids is not None:
                    url += add_ids_to_url(
                        "project_task_temaplte_ids", project_task_template_ids
                    )

                if product_type_ids is not None:
                    url += add_ids_to_url("product_type_ids", product_type_ids)

                url += f"&selection%5Bsessions_cost%5D={sessions_cost}&selection%5Bcontract_cost%5D={contract_cost}&selection%5Bservices_cost%5D={services_cost}&selection%5Bproducts_cost%5D={products_cost}&selection%5Binternal_cost%5D={internal_cost}&selection%5Binternal_product_cost%5D={internal_product_cost}"
                url += f"&company_id={company_id}&token={login_token}"

                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_employee_invoicing_report(
        base_url,
        company_id,
        login_token,
        term_start,
        term_end,
        employee_ids=None,
        customer_ids=None,
        team_id=None,
        product_type_ids=None,
    ):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/report/employee_invoicing?selection%5Bterm_start%5D={term_start}&selection%5Bterm_end%5D={term_end}"

                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&selection%5B{param_name}%5D%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return "".join(
                            f"&selection%5B{param_name}%5D%5B%5D={str(id_)}"
                            for id_ in param_value
                        )
                    return ""

            if employee_ids is not None:
                url += add_ids_to_url("employee_ids", employee_ids)

            if customer_ids is not None:
                url += add_ids_to_url("customer_ids", customer_ids)

            if team_id is not None:
                url += add_ids_to_url("team_id", team_id)

            if product_type_ids is not None:
                url += add_ids_to_url("product_type_ids", product_type_ids)

            url += f"&company_id={company_id}&token={login_token}"

            response = requests.get(url, timeout=ERP.default_timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_work_session_assignments(
        base_url,
        company_id,
        login_token,
        start_date,
        end_date,
        employee_id=None,
        customer_id=None,
        ids=None,
        limit=100,
        offset=0,
    ):
        try:
            with robocorp.log.suppress_variables():
                url = f"{base_url}/work_session/assignments?start_date={start_date}&end_date={end_date}&limit={limit}&offset={offset}"

                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&{param_name}%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return "".join(
                            f"&{param_name}%5B%5D={str(id_)}" for id_ in param_value
                        )
                    return ""

                if employee_id is not None:
                    url += add_ids_to_url("employee_id", employee_id)

                if customer_id is not None:
                    url += add_ids_to_url("customer_id", customer_id)

                if ids is not None:
                    url += add_ids_to_url("ids", ids)

                url += f"&company_id={company_id}&token={login_token}"
                response = requests.get(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return WorkSessionAssignments(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_work_session_assignment(base_url, company_id, login_token, assignment_id):
        try:
            if isinstance(assignment_id, list):
                assignments = []
                for a_id in assignment_id:
                    with robocorp.log.suppress_variables():
                        url = f"{base_url}/work_session/assignments/{a_id}?company_id={company_id}&token={login_token}"
                        response = requests.get(url, timeout=ERP.default_timeout)
                        response.raise_for_status()
                        assignments.append(WorkSessionAssignment(response.json()))
                return assignments
            else:
                with robocorp.log.suppress_variables():
                    url = f"{base_url}/work_session/assignments/{assignment_id}?company_id={company_id}&token={login_token}"
                    response = requests.get(url, timeout=ERP.default_timeout)
                    response.raise_for_status()
                    return WorkSessionAssignment(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def complete_work_session_assignment_requirements(
        base_url,
        company_id,
        login_token,
        assignment=None,
        requirement_id=None,
        customer_id=None,
        date=None,
        completed_by_id=None,
    ):
        try:
            if completed_by_id is None:
                completed_by_id = "75537"
            if assignment:
                if isinstance(assignment, WorkSessionAssignment):
                    requirements = assignment.requirements
                    if len(requirements) > 1:
                        raise ValueError(
                            "This assignment has multiple requirements. Please specify individual requirement details."
                        )
                    elif len(requirements) == 1:
                        requirement = requirements[0]
                        requirement_id = requirement.get("id")
                        customer_id = assignment.customer_id
                        date = assignment.date
                    else:
                        raise ValueError("This assignment has no requirements.")
                else:
                    raise TypeError(
                        "Invalid assignment type. Expected WorkSessionAssignment."
                    )

            if not requirement_id:
                raise ValueError(
                    "Missing required parameter. Please provide a requirement_id"
                )

            with robocorp.log.suppress_variables():
                url = f"{base_url}/work_session/assignments/requirement_complete?company_id={company_id}&token={login_token}&requirement_id={requirement_id}&customer_id={customer_id}&date={date}&completed_by_id={completed_by_id}"
                response = requests.post(url, timeout=ERP.default_timeout)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            raise RuntimeError(
                "Error completing work session assignment requirement"
            ) from e


class Customers:
    def __init__(self, customers):
        self.customers = [Customer(c) for c in customers]

    def id(self, archived=None):
        return [customer.id for customer in self._filter_customers(archived)]

    def name(self, archived=None):
        return [customer.name for customer in self._filter_customers(archived)]

    def get(self, identifier):
        if isinstance(identifier, int):
            return next((c for c in self.customers if c.id == identifier), None)
        else:
            return next(
                (c for c in self.customers if c.name.lower() == identifier.lower()),
                None,
            )

    def _filter_customers(self, archived):
        if archived is None:
            return self.customers
        return [
            customer for customer in self.customers if customer.archived == archived
        ]

    def __repr__(self):
        return str(self.customers)


class Customer:
    def __init__(self, customer_data):
        self.__dict__.update(customer_data)

    def __getattr__(self, name):
        raise AttributeError(f"'Customer' object has no attribute '{name}'")

    def __repr__(self):
        return str(self.__dict__)


class Categories:
    def __init__(self, categories):
        self.categories = categories

    def customers(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            return self._filter_categories_by_id(int(category))[0]["customer_ids"]
        else:
            return self._filter_categories_by_name(category)[0]["customer_ids"]

    def employees(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            return self._filter_categories_by_id(int(category))[0]["employee_ids"]
        else:
            return self._filter_categories_by_name(category)[0]["employee_ids"]

    def category(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            filtered_categories = self._filter_categories_by_id(int(category))
            if not filtered_categories:
                raise ValueError(
                    f"No customer_category with ID '{category}' in customer categories"
                )
            return filtered_categories[0]
        else:
            filtered_categories = self._filter_categories_by_name(category.lower())
            if not filtered_categories:
                raise ValueError(
                    f"No customer category with name '{category}' in customer categories"
                )
            return filtered_categories[0]

    def _filter_categories_by_name(self, name):
        return [
            category
            for category in self.categories
            if category.get("name", "").lower() == name
        ]

    def _filter_categories_by_id(self, category_id):
        return [
            category
            for category in self.categories
            if category.get("id") == category_id
        ]

    def __repr__(self):
        return str(self.categories)


class Groups:
    def __init__(self, groups):
        self.groups = [Group(group) for group in groups]

    def customers(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        group_data = self.group(group)
        return group_data.customer_ids

    def group(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if isinstance(group, int) or (isinstance(group, str) and group.isdigit()):
            group_id = int(group)
            filtered_groups = self._filter_groups_by_id(group_id)
            if not filtered_groups:
                raise ValueError(
                    f"No customer group with ID '{group_id}' in customer groups"
                )
        else:
            filtered_groups = self._filter_groups_by_name(str(group).lower())
            if not filtered_groups:
                raise ValueError(
                    f"No customer group with name '{group}' in customer groups"
                )
        return filtered_groups[0]

    def _filter_groups_by_name(self, name):
        return [group for group in self.groups if group.name.lower() == name]

    def _filter_groups_by_id(self, group_id):
        return [group for group in self.groups if group.id == group_id]

    def __repr__(self):
        return str(self.groups)


class Group:
    def __init__(self, group_data):
        self.__dict__.update(group_data)

    def __getattr__(self, name):
        raise AttributeError(f"'Group' object has no attribute '{name}'")

    def __repr__(self):
        return str(self.__dict__)


class Employees:
    def __init__(self, employees):
        self.employees = [Employee(e) for e in employees]

    def id(self):
        return [employee.id for employee in self.employees]

    def name(self):
        return [employee.name for employee in self.employees]

    def get(self, identifier):
        if isinstance(identifier, int):
            return next((e for e in self.employees if e.id == identifier), None)
        else:
            return next(
                (e for e in self.employees if e.name.lower() == identifier.lower()),
                None,
            )

    def __repr__(self):
        return str(self.employees)


class Employee:
    def __init__(self, employee_data):
        self.__dict__.update(employee_data)

    def __getattr__(self, name):
        raise AttributeError(f"'Employee' object has no attribute '{name}'")

    def __repr__(self):
        return str(self.__dict__)


class EmployeeGroups:
    def __init__(self, groups):
        self.groups = groups

    def employees(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            return self._filter_groups_by_id(int(group))[0]["employee_ids"]
        else:
            return self._filter_groups_by_name(group.lower())[0]["employee_ids"]

    def group(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            filtered_groups = self._filter_groups_by_id(int(group))
            if not filtered_groups:
                raise ValueError(
                    f"No employee group with ID '{group}' in employee groups"
                )
            return filtered_groups[0]
        else:
            filtered_groups = self._filter_groups_by_name(group.lower())
            if not filtered_groups:
                raise ValueError(
                    f"No employee group with name '{group}' in employee groups"
                )
            return filtered_groups[0]

    def _filter_groups_by_name(self, name):
        return [group for group in self.groups if group.get("name", "").lower() == name]

    def _filter_groups_by_id(self, group_id):
        return [group for group in self.groups if group.get("id") == group_id]

    def __repr__(self):
        return str(self.groups)


class EmployeeTeams:
    def __init__(self, teams):
        self.teams = teams

    def employees(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            return self._filter_teams_by_id(int(team))[0]["employee_ids"]
        else:
            return self._filter_teams_by_name(team.lower())[0]["employee_ids"]

    def foremen(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            return self._filter_teams_by_id(int(team))[0]["foreman_ids"]
        else:
            return self._filter_teams_by_name(team.lower())[0]["foreman_ids"]

    def team(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            filtered_teams = self._filter_teams_by_id(int(team))
            if not filtered_teams:
                raise ValueError(f"No employee team with ID '{team}' in employee teams")
            return filtered_teams[0]
        else:
            filtered_teams = self._filter_teams_by_name(team.lower())
            if not filtered_teams:
                raise ValueError(
                    f"No employee team with name '{team}' in employee teams"
                )
            return filtered_teams[0]

    def _filter_teams_by_name(self, name):
        return [team for team in self.teams if team.get("name", "").lower() == name]

    def _filter_teams_by_id(self, team_id):
        return [team for team in self.teams if team.get("id") == team_id]

    def __repr__(self):
        return str(self.teams)


class ProductTypes:
    def __init__(self, product_types):
        self.product_types = [ProductType(pt) for pt in product_types]

    def __getattr__(self, name):
        return [getattr(pt, name) for pt in self.product_types]

    def __repr__(self):
        return str(self.product_types)


class ProductType:
    def __init__(self, product_type_data):
        self.__dict__.update(product_type_data)

    def __getattr__(self, name):
        raise AttributeError(f"'ProductType' object has no attribute '{name}'")

    def __repr__(self):
        return str(self.__dict__)


class WorkSessionAssignments:
    def __init__(self, data):
        self.assignments = [WorkSessionAssignment(a) for a in data]

    def get(self, identifier):
        if isinstance(identifier, int):
            return next((a for a in self.assignments if a.id == identifier), None)
        else:
            return next(
                (a for a in self.assignments if a.name.lower() == identifier.lower()),
                None,
            )

    def __repr__(self):
        return str(self.assignments)


class WorkSessionAssignment:
    def __init__(self, assignment_data):
        self.__dict__.update(assignment_data)

    def __getattr__(self, name):
        raise AttributeError(
            f"'WorkSessionAssignment' object has no attribute '{name}'"
        )

    def __repr__(self):
        return str(self.__dict__)
