# Dummy continuations
ok = -> null
err = (reason) -> console.log("Error: #{reason}")

get_validated_nickname = ->
  nick = $('#nickname').val()
  if nick.length == 0
    alert("Entrez un pseudonyme pour la partie")
    return null
  return nick

Whistiti = (wamp_url="ws://localhost:8080/ws", realm="whistiti") ->
  connection = new autobahn.Connection({url: wamp_url, realm: "whistiti"})
  uuid = null

  card_template = Handlebars.compile($('#card-template').html())
  queued_template = Handlebars.compile($('#queued-template').html())
  scores_template = Handlebars.compile($('#scores-template').html())

  TRANSLATIONS = 

  showPanel = (name) -> $("##{name}-panel").removeClass('hidden')
  hidePanel = (name) -> $("##{name}-panel").addClass('hidden')

  connection.onopen = (session, details) ->
    remote_call = (func, args=[]) ->
      showPanel("loading")
      session.call(func, args).then (ret) ->
        hidePanel("loading")
        ret

    console.log("Connection opened")
    hidePanel('loading')
    showPanel('join')

    # Show waiting players progress bar
    show_queue_size = (queue_size) ->
      $('#queued-panel').html(queued_template({
        'queue_size': queue_size, 'queue_pct': 25*queue_size,
        'queue_remain': 4-queue_size, 'queue_remain_pct': 25*(4-queue_size)
      }))
      showPanel('queued')

    show_my_cards = (cards) ->
      cards.sort (a, b) -> a-b
      for card in cards
        $('#hand-content').append("<li>#{card_template({'cardid': card})}</li>")
      $('.card').click (ev) ->
        $('.card.selected').removeClass('selected')
        $(ev.target).addClass('selected')

    show_players = (players) ->
      for player in players
        if player != get_validated_nickname()
          $('#scores-panel').append(scores_template({'player_name': player}))

    show_cards = (cards) ->
      for card in cards
        $('#hand-content').append(card_template({'cardid': card}))

    $('a.bid').click (ev) ->
      remote_call('bid', [uuid, $(ev.target).attr('data-id')]).then (response) ->
        console.log(JSON.stringify(response))
        if response.error
          alert(response.error)

    $('#join-button').click ->
      nick = get_validated_nickname()
      if ! nick
        return
      console.log("Joining game with nickname #{nick}")
      hidePanel('join')
      remote_call('hello', [nick]).then (response) ->
        show_queue_size(response.queue_size)
        uuid = response.uuid
        console.log("Got UUID #{uuid}")

        # Subscribe to waiting queue growth events (new players join)
        session.subscribe "#{uuid}.queue_growth", (response) ->
          show_queue_size(response[0].queue_size)
        .then(ok, err)

        # Subscribe to game start events
        session.subscribe "#{uuid}.start_game", (response) ->
          hidePanel('queued')
          game = response[0]
          show_my_cards(game.cards)
          show_players(game.players)
          showPanel('scores')
          showPanel('bid')
          console.log(JSON.stringify(response))
        .then(ok, err)

  connection.onclose = (reason, details) ->
    console.log("Connection lost (#{reason})")

  connection.open()

$(document).ready -> Whistiti()