from typing import Self


class BaseMigration:
    next: Self | None = None

    @property
    def migration_id(self):
        return self.__class__.__name__

    async def migrate(self) -> str:
        print(f"Run migration: [{self.migration_id}]")
        await self.upgrade()
        print(f"End migration: [{self.migration_id}]")

        if self.next:
            return await self.next.migrate()
        
        return self.migration_id

    def find_last_migration(self, migration_id: str) -> Self | None:
        if migration_id == self.migration_id:
            return self

        if self.next:
            return self.next.find_last_migration(migration_id)

        return None

    async def upgrade(self):
        pass
