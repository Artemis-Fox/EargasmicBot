const { SlashCommandBuilder } = require("@discordjs/builders")

module.exports = {
	data: new SlashCommandBuilder().setName("pause").setDescription("Pauses the music"),
	run: async ({ client, interaction }) => {
		const queue = client.player.getQueue(interaction.guildId)

		if (!queue) return await interaction.editReply("Sorry hun there are no songs in the queue")

		queue.setPaused(true)
      await interaction.editReply("Fine ill pause :< ")
	},
}
