Приложение "Логирование изменений объектов на уровне БД"
=================================

Установка
--------------
1. На основе абстрактного класса LogProxy из educommon/audit_log/proxies.py создать класс и реализовать его абстрактные 
методы. 

.. code-block:: python

    class AuditLogProxy(LogProxy):
        """Прокси-модель для отображения логов."""

        class Meta:
            proxy = True

        @property
        def user_fullname(self) -> str:
            """Полное имя пользователя."""
            pass

        @property
        def user_organization(self) -> str:
            """Название организации, к которой привязан пользователь."""
            pass


В случае использования сервисной базы для нового класса необходимо реализовать
роутер на основе ServiceDbRouterBase из educommon/django/db/routers.py и добавить его в settings.DATABASE_ROUTERS

.. code-block:: python

    class AuditLogProxyDbRouter(MyServiceDbRouterBase):
        """Роутер базы данных для AuditLogProxy."""

        app_name = 'model_app_name'
        service_db_model_names = {'AuditLogProxy'}


2. На основе абстрактного класса AuditLogPack из educommon/audit_log/actions.py создать класс и реализовать его абстрактные 
методы. В атрибуте model указать модель из пункта "1".

.. code-block:: python

    class AuditPack(AuditLogPack):
        """Журнал изменений."""

        title = 'Журнал изменений (новый)'
        model = AuditLogProxy

        def _make_name_filter(self, field, value):
            """Создает lookup фильтра по фамилии/имени/отчеству пользователя.

            :param str field: название поля ('firstname', 'surname', 'patronymic').
            :param str value: значение, по которому фильтруется queryset.
            """
            pass

Выполнить регистрацию нового пака с помощью контроллера основных приложений проекта.

3. Добавить 'educommon.audit_log.middleware.AuditLogMiddleware', расположив его так, чтобы при его отработке 
в request уже был определен пользователь.

4. Создать и выполнить миграции.
